### update.py
* UPDATE 05/10/2026 - TimmyHeart's ComfyUI patch, optimized for low VRAM (8GB or under) to run large models like WAN 2.2 14B or LTX 2.3 22B
* PUT THIS AT THE END OF "model_management.py" AND REMOVE THE OLD HACK_SPDA
* NOTE: This update might decrease the speed of WAN2.2 14B but will increase the stability further, original speed with old code would generates within 153s/it to 180s/it for WAN2.2 14B and 10s/it to 35s/it for LTX 2.3 22B ( lightning lora, distilled lora, 81 frames, 480x480, 32fps, upscaler to 2k within 20 minutes ) but with this update, the speed will always around 170s/it to 180s/it for WAN 2.2 14B and 60s/it to 100s/it (some steps) for LTX 2.3 22B with the same setup but will have a much more larger shield to prevent OOM.
