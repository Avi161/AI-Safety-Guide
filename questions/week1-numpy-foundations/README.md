# Week 1: NumPy + ML Math Foundations

**Total:** 10 hours | **Focus:** Build ML muscle memory with NumPy

## Learning Objectives

By end of Week 1, you should be able to:

- Vectorize any loop-based computation in NumPy
- Implement core ML operations from scratch (no sklearn)
- Understand broadcasting, reshaping, and matrix operations intuitively
- Code a working linear regression with gradient descent

## Session Schedule

| Session | Notebook | Duration | Focus | Deliverable |
|---------|----------|----------|-------|-------------|
| 1 | `01_numpy_basics.ipynb` | 2 hrs | NumPy fundamentals | 25+ exercises completed |
| 2 | `02_broadcasting_reshaping.ipynb` | 2 hrs | Broadcasting & reshaping | Visualization notebook |
| 3 | `03_linear_algebra.ipynb` | 2 hrs | Linear algebra operations | Matrix ops from scratch |
| 4 | `04_gradient_computation.ipynb` | 2 hrs | Gradient computation | Manual gradient descent |
| 5 | `05_linear_regression.ipynb` | 2 hrs | Mini-project | Linear regression end-to-end |

## Getting Started

```bash
cd week1-numpy-foundations
source venv/bin/activate
jupyter notebook
```

Then open the notebooks in order, starting with `01_numpy_basics.ipynb`.

## Success Criteria

| Criterion | Target | Notes |
|-----------|--------|-------|
| NumPy-100 exercises | 25+ completed | Understand, don't copy |
| Broadcasting | Can predict output shapes | No guessing |
| Matrix ops | 3+ implemented from scratch | Verify with NumPy |
| Gradient descent | Converges on test data | Loss decreases monotonically |
| Linear regression | R² > 0.8 on synthetic data | Match sklearn |
| Documentation | This README + notebook reflections | For future reference |

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Broadcasting errors | Print shapes before every operation |
| Gradient not converging | Check learning rate, normalize data |
| Shape mismatches | Use `.shape` liberally, add assertions |
| Slow loops | Vectorize after understanding the loop version |

## File Structure

```
week1-numpy-foundations/
├── 01_numpy_basics.ipynb              # Session 1
├── 02_broadcasting_reshaping.ipynb    # Session 2
├── 03_linear_algebra.ipynb            # Session 3
├── 04_gradient_computation.ipynb      # Session 4
├── 05_linear_regression.ipynb         # Session 5
├── linear_regression_from_scratch.py  # Standalone module (fill-in-the-blanks)
├── images/                            # Saved visualizations
├── requirements.txt                   # Pinned dependencies
├── venv/                              # Virtual environment
└── README.md                          # This file
```

## Completion Checklist

- [ ] NumPy fundamentals (25+ exercises)
- [ ] Broadcasting visualization saved to `images/`
- [ ] Matrix multiply, outer product, transpose implemented from scratch
- [ ] Gradient descent converges on 1D and 2D functions
- [ ] `LinearRegressionScratch` class fully implemented
- [ ] R² > 0.8 on synthetic data
- [ ] All reflection sections filled in

## Before Week 2

Report back with:
1. Your GitHub repo link
2. One thing that surprised you
3. One concept still fuzzy
4. Your linear regression R² score
