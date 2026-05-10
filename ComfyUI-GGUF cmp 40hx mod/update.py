///////////////////////////////////// UPDATE 05/10/2026 - TimmyHeart's ComfyUI patch, optimized for low VRAM (8GB or under) to run large models like WAN 2.2 14B or LTX 2.3 22B ////////
///////////////////////////////////// PUT THIS AT THE END OF "model_management.py" AND REMOVE THE OLD HACK_SPDA ////////////////////////////
import torch.nn.functional as F
import comfy.model_management as _mm
import math
import logging

_RESERVED_FOR_COMPUTE  = 150           #you could change it to 80
_EXTRA_VRAM_RESERVE    = 50            #you could change it to 10
_CHUNK_SIZE            = 256           #you could change it to 128

_original_min_mem_value = _mm.minimum_inference_memory()

_RESERVED_BYTES = _RESERVED_FOR_COMPUTE * 1024 * 1024           # DO NOT TOUCH
_mm.EXTRA_RESERVED_VRAM = _EXTRA_VRAM_RESERVE * 1024 * 1024     # DO NOT TOUCH

def _new_minimum_inference_memory():
    return _RESERVED_BYTES + _mm.extra_reserved_memory()
_mm.minimum_inference_memory = _new_minimum_inference_memory
_WEAK_DTYPES = (torch.bfloat16, torch.float16)
_original_sdpa = F.scaled_dot_product_attention

def _chunked_f32_attn(q_f32, k_f32, v_f32, scale, mask):
    k_T = k_f32.transpose(-2, -1).contiguous()  # pre-transpose 1 lần
    q_len = q_f32.shape[-2]
    out = torch.empty_like(q_f32)
    for i in range(0, q_len, _CHUNK_SIZE):
        end = min(i + _CHUNK_SIZE, q_len)
        q_c = q_f32[..., i:end, :]
        logits = q_c @ k_T
        logits.mul_(scale)
        if mask is not None:
            mask_slice = mask[..., i:end, :] if mask.dim() >= 2 else mask
            logits.add_(mask_slice)
        attn_w = F.softmax(logits, dim=-1)
        del logits
        out[..., i:end, :] = attn_w @ v_f32
        del attn_w, q_c
    del k_T
    return out

def _universal_hacked_attn(query, key, value, *args, **kwargs):
    orig_dtype = query.dtype
    if orig_dtype not in _WEAK_DTYPES:
        return _original_sdpa(query, key, value, *args, **kwargs)
    q_len = query.shape[-2]
    scale = kwargs.get('scale') or (1.0 / math.sqrt(query.size(-1)))
    attn_mask = kwargs.get('attn_mask')
    q_f32 = query.to(torch.float32)
    k_f32 = key.to(torch.float32)
    v_f32 = value.to(torch.float32)
    if q_len > 4096:
        out_f32 = _chunked_f32_attn(q_f32, k_f32, v_f32, scale, attn_mask)
        del q_f32, k_f32, v_f32
    else:
        mask_f32 = None
        if attn_mask is not None and isinstance(attn_mask, torch.Tensor):
            if attn_mask.dtype in _WEAK_DTYPES:
                mask_f32 = attn_mask.to(torch.float32)
            else:
                mask_f32 = attn_mask
        out_f32 = _original_sdpa(q_f32, k_f32, v_f32, *args,
                                  **{**kwargs, 'attn_mask': mask_f32})
        del q_f32, k_f32, v_f32
    res = out_f32.to(orig_dtype)
    del out_f32
    return res
F.scaled_dot_product_attention = _universal_hacked_attn
# comfy.ops wrapper — để WAN đi qua được
try:
    import comfy.ops
    comfy.ops.scaled_dot_product_attention = _universal_hacked_attn
    logging.info("[CMP] comfy.ops.sdpa patched.")
except (ImportError, AttributeError):
    pass
# xformers
try:
    import xformers.ops
    _original_xformers = xformers.ops.memory_efficient_attention
    def _hacked_xformers(query, key, value, *args, **kwargs):
        orig_dtype = query.dtype
        if orig_dtype not in _WEAK_DTYPES:
            return _original_xformers(query, key, value, *args, **kwargs)
        q_f32 = query.to(torch.float32)
        k_f32 = key.to(torch.float32)
        v_f32 = value.to(torch.float32)
        if "attn_bias" in kwargs and isinstance(kwargs["attn_bias"], torch.Tensor):
            if kwargs["attn_bias"].dtype in _WEAK_DTYPES:
                kwargs = {**kwargs, "attn_bias": kwargs["attn_bias"].to(torch.float32)}
        out = _original_xformers(q_f32, k_f32, v_f32, *args, **kwargs)
        del q_f32, k_f32, v_f32
        res = out.to(orig_dtype)
        del out
        return res
    xformers.ops.memory_efficient_attention = _hacked_xformers
    logging.info("[CMP] Xformers patched.")
except ImportError:
    pass
_new_min_mem_value = _new_minimum_inference_memory()
_saved_vram = _original_min_mem_value - _new_min_mem_value
logging.info(
    f"[CMP] minimum_inference_memory pulled down to: {_new_min_mem_value / 1024**2:.0f} MB "
    f"(Just cut: {_original_min_mem_value / 1024**2:.0f} MB)."
)
logging.info(
    f"[CMP] Successfully stole {_saved_vram / 1024**2:.0f} MB VRAM for extra Weight into GPU!"
)
