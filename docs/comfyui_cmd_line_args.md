## ComfyUI Command Line Arguments

Usage Example: **-python main.py --auto-launch --lowvram**

- **-h, --help**

  show this help message and exit

- **--listen [IP]**

  Specify the IP address to listen on (default: 127.0.0.1) If --listen is provided without an argument, it defaults to 0.0.0.0 (listens on all)

- **--port PORT**

  Set the listen port

- **--tls-keyfile TLS_KEYFILE**

  Path to TLS (SSL) key file Enables TLS, makes app accessible at https://... requires --tls-certfile to function

- **--tls-certfile TLS_CERTFILE**

  Path to TLS (SSL) certificate file Enables TLS, makes app accessible at https://... requires --tls-keyfile to function

- **--enable-cors-header [ORIGIN]**

  Enable CORS (Cross-Origin Resource Sharing) with optional origin or allow all with default '*'

- **--max-upload-size MAX_UPLOAD_SIZE**

  Set the maximum upload size in MB

- **--extra-model-paths-config PATH [PATH ...]**

  Load one or more extra_model_paths.yaml files

- **--output-directory OUTPUT_DIRECTORY**

  Set the ComfyUI output directory

- **--temp-directory TEMP_DIRECTORY**

  Set the ComfyUI temp directory (default is in the ComfyUI directory)

- **--input-directory INPUT_DIRECTORY**

  Set the ComfyUI input directory

- **--auto-launch**

  Automatically launch ComfyUI in the default browser

- **--disable-auto-launch**

  Disable auto launching the browser

- **--cuda-device DEVICE_ID**

  Set the id of the cuda device this instance will use

- **--cuda-malloc**

  Enable cudaMallocAsync (enabled by default for torch 2.0 and up)

- **--disable-cuda-malloc**

  Disable cudaMallocAsync

- **--force-fp32**

  Force fp32 (If this makes your GPU work better please report it)

- **--force-fp16**

  Force fp16

- **--bf16-unet**

  Run the UNET in bf16 This should only be used for testing stuff

- **--fp16-unet**

  Store unet weights in fp16

- **--fp8_e4m3fn-unet**

  Store unet weights in fp8_e4m3fn

- **--fp8_e5m2-unet**

  Store unet weights in fp8_e5m2

- **--fp16-vae**

  Run the VAE in fp16, might cause black images

- **--fp32-vae**

  Run the VAE in full precision fp32

- **--bf16-vae**

  Run the VAE in bf16

- **--cpu-vae**

  Run the VAE on the CPU

- **--fp8_e4m3fn-text-enc**

  Store text encoder weights in fp8 (e4m3fn variant)

- **--fp8_e5m2-text-enc**

  Store text encoder weights in fp8 (e5m2 variant)

- **--fp16-text-enc**

  Store text encoder weights in fp16

- **--fp32-text-enc**

  Store text encoder weights in fp32

- **--directml [DIRECTML_DEVICE]**

  Use torch-directml

- **--disable-ipex-optimize**

  Disables ipex.optimize when loading models with Intel GPUs

- **--preview-method [none,auto,latent2rgb,taesd]**

  Default preview method for sampler nodes

- **--use-split-cross-attention**

  Use the split cross attention optimization Ignored when xformers is used

- **--use-quad-cross-attention**

  Use the sub-quadratic cross attention optimization Ignored when xformers is used

- **--use-pytorch-cross-attention**

  Use the new pytorch 2.0 cross attention function

- **--disable-xformers**

  Disable xformers

- **--force-upcast-attention**

  Force enable attention upcasting, please report if it fixes black images

- **--dont-upcast-attention**

  Disable all upcasting of attention Should be unnecessary except for debugging

- **--gpu-only**

  Store and run everything (text encoders/CLIP models, etc... on the GPU)

- **--highvram**

  By default models will be unloaded to CPU memory after being used This option keeps them in GPU memory

- **--normalvram**

  Used to force normal vram use if lowvram gets automatically enabled

- **--lowvram**

  Split the unet in parts to use less vram

- **--novram**

  When lowvram isn't enough

- **--cpu**

  To use the CPU for everything (slow)

- **--disable-smart-memory**

  Force ComfyUI to aggressively offload to regular ram instead of keeping models in vram when it can

- **--deterministic**

  Make pytorch use slower deterministic algorithms when it can Note that this might not make images deterministic in all cases

- **--dont-print-server**

  Don't print server output

- **--quick-test-for-ci**

  Quick test for CI

- **--windows-standalone-build**

  Windows standalone build: Enable convenient things that most people using the standalone windows build will probably enjoy (like auto opening the page on startup)

- **--disable-metadata**

  Disable saving prompt metadata in files

- **--multi-user**

  Enables per-user storage

- **--verbose**

  Enables more debug prints
