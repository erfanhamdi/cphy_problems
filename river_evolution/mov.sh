ffmpeg -r 60 -i /Users/venus/Erfan/data-driven-course/cphy_problems/river_evolution/figs/river_evolution_%04d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -pix_fmt yuv420p /Users/venus/Erfan/data-driven-course/cphy_problems/river_evolution/vid2.mov
