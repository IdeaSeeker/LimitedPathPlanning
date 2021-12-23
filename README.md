# Path planning in a limited observable environment algorithms (LPA*, D* Lite)

## Description

A software project for Heuristic algorithms course at the SPbU.
LPA* and D* Lite algorithms for path planning in a limted observable environment. 

## Installation

Clone repository:

```bash
git clone git@github.com:IdeaSeeker/LimitedPathPlanning.git
```

Install requirements.txt:

```bash
cd LimitedPathPlanning
pip install -r requirements.txt
```

## Usage

### Example

```bash
python src/main.py dstarlite data/lak105d.map output --gif_speed 150
```

Your resulting gifs would be in the repository root.

### Arguments description

```bash
python src/main.py -h

usage: main.py [-h] [--vision_distance VISION_DISTANCE] [--n_tasks N_TASKS] [--pixel_size PIXEL_SIZE] [--gif_speed GIF_SPEED] {dstarlite,lpastar} map_path output_path

positional arguments:
  {dstarlite,lpastar}   algorithm to be used
  map_path              path to the .map file. scenario file .map.scen should be nearby
  output_path           path to resulting gif folder

optional arguments:
  -h, --help            show this help message and exit
  --vision_distance VISION_DISTANCE
                        dstarlite vision distance
  --n_tasks N_TASKS     number of scenarios to run
  --pixel_size PIXEL_SIZE
                        output gif pixel size
  --gif_speed GIF_SPEED
                        milliseconds between gif frames
```

## Input

Our program uses maps and tasks in the MovingAI format.

You can find it [here](https://movingai.com/benchmarks/formats.html).

Examples could be found in **data** folder.

## Output

Out program ouputs gifs with task. **output_path** argument points to their location.

Examples could also be found in **output** folder.

## D* Lite running examples

- map **/data/lak105d.map**
<img src="/output/dstarlite.gif"/>

 - map **/data/den312d.map** with `vision_radius = 1`
<img src="/output/d_star_lite_vision_1.gif"/>

- map **/data/den312d.map** with `vision radius = 5`
<img src="/output/d_star_lite_vision_5.gif"/>


## LPA* running example

- map **/data/lak105d.map**

- legend:
  - start - red point
  - finish - green point
  - appearing obstacles - black points
  - reopened cells - gray points

<img src="/output/lpastar.gif"/>

## References

+ Koenig, S. Likhachev, M. and Furcy, D. 2004. Lifelong Planning A*. Artificial Intelligence, 155(1-2), pp. 93-146. [URL](https://www.cs.cmu.edu/~maxim/files/aij04.pdf)

+ Sven Koenig and Maxim Likhachev. 2002. D*lite. In Eighteenth national conference on Artificial intelligence (AAAI 2002). 476–483. [URL](http://idm-lab.org/bib/abstracts/papers/aaai02b.pdf)

## Participants

### Mentor

Yakovlev Konstantin Sergeevich

### Students

Kharlapenko Dmitrii

Stroganov Nikita

## Large D* Lite running example with increased visibility radius

<img src="/output/paris_vision_10.gif"/>
