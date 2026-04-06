# L-Shape Visibility Probability (3/2 Square Puzzle)

An interactive 3D visualization of the geometric probability problem: two random points in an L-shaped region (unit square with top-right quadrant removed).

## Problem Statement

Given an L-shaped region formed by removing the top-right quadrant [0.5,1]×[0.5,1] from the unit square [0,1]×[0,1], what is the probability that two randomly selected points can see each other without their line of sight crossing the removed region?

**Answer: P(good) = 8/9**

## The Mathematics

### Key Insight: Unit Square Ray Problem

A ray enters a unit square from corner (1,0) at a random exit point. The average visible area to the left of the ray is:

**Case 1: Ray exits LEFT edge at (0,y)**
- Visible area (triangle): A = y/2
- Average: ∫₀¹ (y/2) dy = **1/4**

**Case 2: Ray exits TOP edge at (x,1)**
- Visible area (trapezoid): A = (1+x)/2
- Average: ∫₀¹ ((1+x)/2) dx = **3/4**

**Combined Average:**
- Average Area = (1/2)(1/4) + (1/2)(3/4) = **1/2**

This **1/2 average visibility** extends to the L-shape problem, giving us P(good) = 8/9.

### Quadrant Visibility Heights

The 3D prism visualization shows visibility as a percentage of maximum (which is 3 quadrants):

- **Q1** (always sees all 3): height = 1.0 (100%)
- **Q2** (sees Q1 + Q2 + avg 0.5 of Q3): height = 5/6 (83.3%)
- **Q3** (sees Q1 + Q3 + avg 0.5 of Q2): height = 5/6 (83.3%)
- **Stacked Q2+Q3**: 5/6 + 5/6 = 5/3 ≈ 1.667

## Controls

- **Drag to rotate** the 3D view
- **Scroll to zoom** (scroll out for full view)
- **Right-click drag to pan**
- **📍 Top View**: Look down from above
- **↺ Reset View**: Return to default perspective
- Hover over prisms to see visibility details

## Visualization Details

The three quadrants are represented as stacked prisms:

- **Q1 (bottom-left)**: Uniform blue, always 100% visibility
- **Q2 (bottom-right)**: Blue to green gradient, 83.3% average visibility
- **Q3 (top-left)**: Blue to green gradient, 83.3% average visibility (rotated 270°)

Color represents visibility percentage:
- 🔵 Blue = Low visibility
- 🟢 Green = High visibility

## Technical Details

Built with:
- **Three.js** for 3D rendering
- Vanilla JavaScript with no dependencies (except Three.js)
- Self-contained HTML file

## Deployment

This project is ready for GitHub Pages. Simply push to GitHub and enable Pages in your repository settings.

To run locally: Open `index.html` in any modern web browser.

## Problem Source

Geometric probability on an L-shaped region with visibility constraints.
