#!/bin/bash
while true; do
    ffmpeg -i "/home/pavel/.config/meowrch/videos/totoro.mp4" \
        -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
        -f image2pipe \
        -vcodec png \
        -r 30 \
        - 2>/dev/null | swww img - \
        --transition-bezier '.43,1.19,1,.4' \
        --transition-type 'grow' \
        --transition-duration '0.4' \
        --transition-fps 144 \
        --invert-y \
        --transition-pos '1573, 799'
done
