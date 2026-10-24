# Grid Rendering Benchmarks

These benchmarks compare the grid-rendering approaches used in [`run.py`](../run.py)
and [`src/graphics_engine/core/main.py`](../src/graphics_engine/core/main.py):

- **Pygame:** draw each vertical grid line with `pygame.draw.line`.
- **NumPy:** use `pygame.surfarray.pixels3d` to color vertical slices of the
  canvas. Grid X coordinates are calculated before the timed run.

The benchmark renders the background, grid, and circle to a high-resolution
canvas, smooth-scales it to the window size, blits it, and flips the display.
Frame-rate caps are disabled so the measurements reflect rendering throughput,
not the differing `Clock.tick()` limits in the original scripts.

## Grid implementation comparison

Measured fullscreen at **1920×1080**, with three 2-second trials per method and
scale and a 0.5-second warmup before each trial. FPS values are trial means.

| Scale | Pygame grid (FPS) | NumPy grid (FPS) | NumPy relative to Pygame |
| ---: | ---: | ---: | ---: |
| 1× | 106.04 | 104.01 | 2.03 FPS slower (1.9%) |
| 2× | 41.13 | 38.26 | 2.87 FPS slower (7.0%) |
| 4× | 17.60 | 15.92 | 1.68 FPS slower (9.6%) |

Pygame's line drawing was faster in all three measurements. At 1×, the
difference is small: it is less than the run-to-run variation observed in the
trials, so that result does not establish a reliable advantage. At 2× and 4×,
Pygame was consistently faster in the measured trials. These results apply to
this rendering workload and environment; they do not show that one technique
will always be faster on other machines or for other surface formats.

## Pygame grid performance by window size

The following benchmark uses only Pygame grid drawing. Each display mode was
set once and kept in place while its three scales were measured. The fullscreen
size was **1920×1080**. As above, each FPS value is the mean of three uncapped
2-second trials, with a 0.5-second warmup before each trial. The `±` value is
the sample standard deviation of the three trial FPS results.

| Window size | Scale 1 (FPS) | Scale 2 (FPS) | Scale 4 (FPS) |
| --- | ---: | ---: | ---: |
| 640×480 | 1,628 ± 238 | 298 ± 6 | 104 ± 5 |
| 800×600 | 1,064 ± 78 | 193 ± 3 | 69 ± 2 |
| 1600×900 | 163 ± 6 | 55 ± 1 | 23 ± 0.1 |
| Fullscreen (1920×1080) | 95 ± 1 | 38 ± 0.5 | 16 ± 0.3 |

## Performance analysis

- **Increasing scale reduces FPS at every window size.** The high-resolution
  canvas contains `window width × window height × scale²` pixels. A 4× scale
  therefore has 16 times as many canvas pixels as 1×, increasing the amount of
  work involved in filling, drawing, and smooth-scaling the canvas.
- **Larger windows generally reduce FPS.** They require more pixels to be
  rendered and smooth-scaled. For example, at 2× the measured mean falls from
  298 FPS at 640×480 to 193 FPS at 800×600, 55 FPS at 1600×900, and 38 FPS at
  fullscreen 1920×1080.
- **The grid-method gap is smaller than the total rendering cost at higher
  scales.** At fullscreen, replacing NumPy slices with Pygame lines improved
  measured mean FPS by about 2 FPS at 1× and 2×, and about 1.7 FPS at 4×.
  Increasing scale and output resolution have a much more pronounced impact
  than the choice between these two grid implementations in this test.
- **Small-window scale-1 results are less stable.** Their trial-to-trial
  variation is noticeably higher than most other entries. With uncapped
  rendering and very high FPS, scheduling and window/display overhead can be a
  larger part of a short measurement. Treat those means as approximate.

These are throughput measurements from one system and one set of trials, not
guaranteed performance figures. Display drivers, compositing, hardware, and
Pygame/SDL builds can all affect the results. In particular, the FPS numbers
are uncapped and should not be interpreted as the refresh rate or as expected
gameplay FPS when a frame cap or VSync is enabled.
