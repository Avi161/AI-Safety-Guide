# Week 1: NumPy + ML Math Foundations

**Total:** ~14 hours (no hurry — depth over speed) | **Focus:** Build ML muscle memory and expert-level intuition with NumPy via many anchor tasks

## Learning Objectives

By end of Week 1, you should be able to:

- Vectorize any loop-based computation in NumPy
- Implement core ML operations from scratch (no sklearn)
- Understand broadcasting, reshaping, and matrix operations intuitively
- Code a working linear regression with gradient descent

## Design: Accelerated Expertise

This week is structured using principles from *Accelerated Expertise: Training for High Proficiency in a Complex World* (Hoffman et al.) to speed up transfer to real ML work:

- **Case-first:** Each session starts with a concrete ML-style task (e.g. weighted sum, center features, one gradient step) instead of a long list of basics. You build the mental model by doing the task, then see the pattern again in later sessions.
- **Worked example → your turn:** We show one full solution with expert reasoning (shapes, why this op), then you do a variation (different sizes, same idea).
- **Just-in-time concepts:** Short “Concept” boxes (array, shape, broadcasting, matvec) appear when a case needs them, not in a big block up front.
- **Sensemaking:** After each case you reflect (“What would break if…?”, “What cues told you…?”) instead of only checking a single correct answer. This supports learning from messy, real-world feedback later.
- **Connections:** Sessions 3–5 explicitly link back to earlier cases (“This is the same as Session 4”; “predict is the same as Session 3”) so knowledge stays flexible and transferable.

## Session Schedule

| Session | Notebook | Duration | Focus | Deliverable |
|---------|----------|----------|-------|-------------|
| 1 | `01_numpy_basics.ipynb` | ~3 hrs | 4 anchor cases: weighted sum, normalise, mask indexing, view vs copy | Reference exercises + reflections |
| 2 | `02_broadcasting_reshaping.ipynb` | ~3 hrs | 3 anchor cases: center features, row norm, outer product | Predict shapes, visualization |
| 3 | `03_linear_algebra.ipynb` | ~3 hrs | 3 anchor cases: LR step, batch weights, numerical gradient check | Matrix ops from scratch |
| 4 | `04_gradient_computation.ipynb` | ~3 hrs | 3 anchor cases: full GD, numerical check, learning rate | 1D/2D GD + LR from scratch |
| 5 | `05_linear_regression.ipynb` | ~2.5 hrs | Capstone + debug buggy code + sklearn comparison | Linear regression end-to-end, R² > 0.8 |

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
| Mental model | Can explain why a piece of ML code uses a given shape or operation | e.g. “We use (n,1) so broadcasting adds one bias per row” |
| Debugging | Can fix a shape error using your mental model | Inspect shapes, match dimensions, don’t guess |
| NumPy-100 / reference | Completed anchor cases + reference exercises as needed | Understand, don’t copy |
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
