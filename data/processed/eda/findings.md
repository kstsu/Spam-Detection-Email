# EDA Findings

Raw rows: 4601; exact duplicate rows removed: 391; conflicting duplicate groups: 3; cleaned rows: 4210.

- The cleaned data remains mildly imbalanced, so stratification and spam-class F1 are used.
- Feature families use different units and scales, supporting scaling inside the linear and probabilistic pipelines.
- Several word and symbol features differ substantially by class, motivating content-plus-symbol inputs.
- Correlated feature groups are present, so model comparison includes both a linear model and a tree ensemble.
- Capital totals are strongly skewed; extreme values are retained as potentially legitimate email style rather than deleted without evidence.
