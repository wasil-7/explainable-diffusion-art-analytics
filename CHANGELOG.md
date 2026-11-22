# Final implementation changelog

Every manuscript replacement is recorded below. Table and figure diffs/source hashes supplement these records.

## 1. T0 author block

Reason: Equal centered author columns, exact names/department, no roll-number or duplicate affiliation footnote.

Before:

```text
\author{Muhammad Wasil Kayani and Umar Asghar\thanks{The authors are with the Department of Computer Science (BS Data Science, Section DSB), National University of Computer and Emerging Sciences (FAST-NUCES), Islamabad, Pakistan. E-mail: i242551@nu.edu.pk; i242532@nu.edu.pk. }}
```

After:

```text
\author{\begin{tabular}{@{}c@{\hspace{0.45in}}c@{}}
Wasil Kayani & Umar Asghar\\[3pt]
\normalsize Department of AI \& Data Science & \normalsize Department of AI \& Data Science\\
\normalsize FAST-NUCES, Islamabad, Pakistan & \normalsize FAST-NUCES, Islamabad, Pakistan\\
\normalsize i242551@nu.edu.pk & \normalsize i242532@nu.edu.pk
\end{tabular}}
```

## 2. T0 PDF metadata

Reason: Match author spelling and preserve title.

Before:

```text
\usepackage[hidelinks]{hyperref}
```

After:

```text
\usepackage[hidelinks]{hyperref}
\hypersetup{pdfauthor={Wasil Kayani and Umar Asghar},pdftitle={Explainable Visual Analytics and Forensic Shortcut Auditing of Human and Diffusion Artwork Across Art-Historical Movements}}
```

## 3. \begin{abstract}

Reason: T8/T11 define AUROC/F1/FFT, retain numbers, give the negative finding plainly.

Before:

```text

Diffusion artwork detection can achieve high predictive accuracy without identifying which visual differences survive benchmark confounds. This study develops a twelve-step explainable visual analytics framework combining mathematical features, grouped evaluation, neighborhood diagnostics and a mandatory control-variable gate. An exhaustive AI-ArtBench audit covers 185,015 files; a balanced cohort contains 45,000 artworks, with a native-$256^2$ Human--Latent Diffusion primary cohort of 30,000 and 6,000 held-out test images. A 104-feature logistic probe attains AUROC 0.9824 and F1 0.9420, outperforming FFT-only features (AUROC 0.6839) but trailing frozen ResNet-50 (0.9999) and DINOv2 (0.9997). The handcrafted AUROC gain over FFT-only is 0.2985. Across 1,040 within-style feature comparisons, 542 satisfy an exploratory statistical rule. However, metadata AUROC 1.0000 exposes origin-aligned JPEG quantization, and verified subject matches are unavailable; consequently no comparison is eligible for confirmatory diffusion-origin attribution. Removing ordinal features reduces AUROC to 0.9080, a decrease of 0.0744, while JPEG-quality-50 recompression reduces it to 0.6819. Linked artwork views, uncertainty summaries and explicit projection fidelity make these associations inspectable. The contribution is a reproducible descriptive atlas and forensic diagnosis of shortcut availability, rather than confirmation of an encoding-independent origin effect.

```

After:

```text

Diffusion-artwork detection can rank benchmark origins accurately without isolating which differences survive source confounds. This study combines named image measurements, grouped evaluation, projection diagnostics and a common-support gate. An exhaustive AI-ArtBench audit covers 185,015 files; a balanced tier contains 45,000 artworks, including a native-$256^2$ Human--Latent Diffusion primary cohort of 30,000 with 6,000 held-out test images. A 104-feature logistic probe attains area under the receiver operating characteristic curve (AUROC) 0.9824 and F1, the harmonic mean of precision and recall, 0.9420. It trails frozen ResNet-50 (0.9999) and DINOv2 (0.9997), while exceeding the internal fast Fourier transform (FFT)-only comparator by 0.2985 AUROC. Of 1,040 within-style feature comparisons, 542 meet an exploratory statistical rule. Metadata AUROC 1.0000 reveals origin-aligned technical information, but JPEG common support and verified subject matches are absent; no comparison is eligible for confirmatory diffusion-origin attribution. Removing ordinal features reduces AUROC by 0.0744 to 0.9080; JPEG-quality-50 recompression reduces it to 0.6819. Linked artwork views and measured projection fidelity make these associations inspectable. The contribution is a descriptive atlas and a negative validity audit, not confirmation of an encoding-independent origin effect.

```

## 4. T1 Introduction availability

Reason: Remote has no refs; distinguish prepared local release from a completed upload.

Before:

```text
Code and reproducibility artifacts are released through the official repository
```

After:

```text
Code and reproducibility artifacts are prepared for the official repository
```

## 5. T5 contribution 2

Reason: Lead with stronger frozen baselines, then label the internal comparator correctly.

Before:

```text
A four-family, 104-predictor representation with linked visual diagnostics; AUROC 0.9824 exceeds the identically evaluated FFT-only probe by 0.2985.
```

After:

```text
A transparent 104-predictor probe (AUROC 0.9824), trailing ResNet-50 by 0.0175 (95\% interval $[-0.0216,-0.0140]$) and DINOv2 by 0.0173, while exceeding FFT-only, a matched internal ablation comparator, by 0.2985.
```

## 6. \subsection{Artwork Benchmarks and Complexity--Entropy Aesthetics}

Reason: T4 thematic establishment, limitation and precise study difference; T11 verified JPEG-bias context.

Before:

```text

ArtBrain \cite{p1} provides joint artwork/source tasks, whereas entropy--complexity coordinates \cite{p2} describe platform art. Historical latent representations \cite{p11} and artwork self-distillation \cite{p16} add context and saliency. Their tasks differ from matched binary ranking; formal coordinates do not establish semantic or chronological interpretation.


```

After:

```text

ArtBrain \cite{p1} establishes artwork/source prediction, while complexity--entropy coordinates \cite{p2}, historical latent representations \cite{p11} and self-distilled saliency \cite{p16} support formal or contextual description. Their joint-label, observational or context-prediction tasks do not establish matched binary origin effects. This study instead compares named within-style measurements on frozen grouped Human--LD identities. It treats entropy and complexity as descriptors, not aesthetic merit or chronology.


```

## 7. \subsection{Spectral, Wavelet and Color Forensics}

Reason: T4 thematic establishment, limitation and precise study difference; T11 verified JPEG-bias context.

Before:

```text

SCADET \cite{p4}, SPAI \cite{p5} and FIRE \cite{p6} learn spectral/reconstruction evidence; SIDWA \cite{p14} learns wavelet attention and CoDA \cite{p8} probes color. The present fixed descriptors expose named measurements and conditional family contributions rather than reproducing those trained architectures or assuming compression invariance.


```

After:

```text

SCADET \cite{p4}, SPAI \cite{p5} and FIRE \cite{p6} establish learned frequency or reconstruction evidence; SIDWA \cite{p14} learns wavelet attention and CoDA \cite{p8} probes color. Different training, crop contexts and domains prevent direct attribution of those scores to our fixed measurements. The present FFT/Haar/color families expose conditional contributions without reproducing these networks. Grommelt et al. \cite{jpeg_bias} demonstrate JPEG/size bias on GenImage; that prior finding motivates encoding checks but does not prove that our pixel probes use the available JPEG association.


```

## 8. \subsection{Alignment, Generalization and Grounding}

Reason: T4 thematic establishment, limitation and precise study difference; T11 verified JPEG-bias context.

Before:

```text

B-Free \cite{p3} motivates content controls and VIB-Net \cite{p7} targets generalization. FakeBench \cite{p12}, pixel-inconsistency localization \cite{p13} and region reasoning \cite{p15} provide richer supervised grounding than the unverified semantic labels available here. Their AP, localization and explanation endpoints cannot be ranked as artwork AUROC.


```

After:

```text

B-Free \cite{p3} establishes content-aligned training and VIB-Net \cite{p7} tests detector generalization. FakeBench \cite{p12}, pixel-inconsistency localization \cite{p13} and region reasoning \cite{p15} provide supervised explanations or localization beyond the semantic labels available here. Their photographic, AP, localization and explanation endpoints do not form a matched artwork-AUROC comparison. This study exposes missing subject support explicitly and links release-labeled errors to pixels; it claims neither equivalent content alignment nor unseen-generator performance.


```

## 9. \subsection{Scalable and Diagnostic Visual Analytics}

Reason: T4 thematic establishment, limitation and precise study difference; T11 verified JPEG-bias context.

Before:

```text

PixelatedScatter \cite{p9} informs count-aware display abstraction; MisVisFix \cite{p10} motivates visible diagnostics. Neither validates this artwork embedding or interface. Neighborhood fidelity is measured separately. Table~\ref{tab:t1} summarizes the sixteen studies; claims follow the collected manuscript versions, with verified publication metadata in References.


```

After:

```text

PixelatedScatter \cite{p9} establishes count-aware display abstraction, while MisVisFix \cite{p10} supports visible chart diagnostics. Their display/user-task evaluations do not establish the fidelity or usefulness of this artwork interface. The present workflow measures neighborhood preservation separately and links fixed-axis views to actual quadrant evidence, without claiming a user-study benefit. Table~\ref{tab:t1} summarizes the sixteen reviewed studies with published years and marked manuscript-version evidence.


```

## 10. T9 twelve-step/algorithm mapping

Reason: Resolve planned versus executable numbering without inventing a new execution order.

Before:

```text
Algorithm~\ref{alg:pipeline} preserves the twelve-step planned workflow, including a descriptive restriction whenever subject matching is uncertain.
```

After:

```text
Algorithm~\ref{alg:pipeline} implements the planned twelve-step workflow. Planned steps 1--3 map to the input and lines 1--3/6; step 4 to lines 4--7; step 5 to line 8; steps 6--7 to lines 9--10/16; steps 8--9 to lines 11--15; and steps 10--12 to line 16 and the output.
```

## 11. T9 Algorithm line 8

Reason: Replace undefined Step 5 label by the actual operation.

Before:

```text
Evaluate Step 5 technical, subject and JPEG common-support gates
```

After:

```text
Evaluate technical, subject and JPEG common-support gates
```

## 12. T8 first definitions

Reason: Define eligibility and exploratory status once before the decision rule.

Before:

```text
Let $G$ indicate satisfied subject, native-size, style, encoding and support controls. Confirmatory eligibility requires
```

After:

```text
Let $G$ indicate satisfied subject, native-size, style, encoding and support controls. A comparison is gate-eligible only when these controls hold; an exploratory pass meets the statistical rule without verified controls. Confirmatory eligibility requires
```

## 13. T8 frozen-fit definition

Reason: State what uncertainty includes rather than relying on shorthand.

Before:

```text
Intervals adapt bootstrap resampling \cite{bootstrap} to 1,000 whole-source-group draws;
```

After:

```text
Intervals adapt bootstrap resampling \cite{bootstrap} to 1,000 whole-source-group draws; conditional on frozen fits means that fitted preprocessing, model parameters and thresholds are held fixed during resampling.
```

## 14. \subsection{Refinements to the Planned Methodology}

Reason: T7 verify each plan step; distinguish genuine departures, calibrated choices and omitted reporting.

Before:

```text

Refinements comprise NumPy Lloyd clustering, a combined HSV+Lab family with isolated ablations, whole-source-group randomization and paired fixed-geometry silhouette bootstraps. The released \texttt{manuscript/tables/changes.csv} records their validity costs; none repairs absent controls.
Separate leave-artist, leave-style and unseen-generator experiments were promised but not run. Known artist families are split-disjoint, which does not substitute for those protocols. AI numeric filename prefixes are conservative groups, not verified prompt IDs. No GAN cohort, independently annotated material labels or dashboard user study was implemented. These departures limit the scope of the implemented evaluation.


```

After:

```text

The plan's four disjoint quadrants remain primary; five overlapping crops add a sensitivity, while the full-canvas comparison also changes dimensionality. The planned development calibration selects $\tau_S=0.01$ from a 0.05 starting cutoff; this is not a fixed-cutoff violation. Combining HSV+Lab changes the primary family definition, so isolated color ablations bound that choice. NumPy Lloyd clustering substitutes for a blocked library implementation; paired silhouette intervals reuse cached geometry rather than recomputing distances.

Separate artist/style/generator holdouts and the GAN arm were not run; source groups and AI-prefix proxies do not establish those generalizations or verified prompts. Missing subjects and JPEG overlap restrict all contrasts to description; whole-group randomization lacks verified exchangeability. The planned movement-by-generator output is a Human--LD style-family heatmap, with resized SD only descriptive. Eight primary cases replace a generator-spanning gallery; semantic/material labels and a user study are unavailable. Dispersion ratios and inter-style centroid distances are cached but omitted from the main results to prioritize control evidence. The released \texttt{results/changes.csv} checks all twelve steps and records these limits and completed stretch analyses.


```

## 15. T12 probe naming

Reason: Define Metadata-only once and retain exact implementation correspondence.

Before:

```text
Five logistic probes use identical 6,000 test IDs: handcrafted 104-D, FFT-only 36-D, metadata, frozen ResNet-50 \cite{resnet} 2,048-D and frozen DINOv2 \cite{dinov2} ViT-S/14 384-D.
```

After:

```text
Five logistic probes use identical 6,000 test IDs: Handcrafted (104-D), FFT-only (36-D), Metadata-only (the implementation's \texttt{metadata\_gated} probe), frozen ResNet-50 \cite{resnet} 2,048-D and frozen DINOv2 \cite{dinov2} ViT-S/14 384-D.
```

## 16. T9 revision provenance

Reason: Flag additional manuscript summaries; metadata is not misdescribed as a learned feature.

Before:

```text
\section{Results and Analysis}
```

After:

```text
Relative to the preceding report, aggregate probe intervals, paired differences, five grouped repartitions, mixed-cohort F1 and JPEG quantization means are additional manuscript summaries from the same cached features, predictions and metadata; no new data were collected. Released scripts and CSVs identify their provenance.

\section{Results and Analysis}
```

## 17. T2 results reference

Reason: Add companion metrics table to the narrative.

Before:

```text
Table~\ref{tab:t4} reports all primary metrics and validation-selected settings;
```

After:

```text
Tables~\ref{tab:t4} and \ref{tab:essential} report primary metrics and validation-selected settings;
```

## 18. T2 accuracy/precision/recall table

Reason: Self-contained metrics are read from the original full per-probe CSV.

Before:

```text
\input{tables/table_04.tex}
```

After:

```text
\input{tables/table_04.tex}
\input{tables/essential_metrics.tex}
```

## 19. T11 precise metadata result

Reason: Do not imply that the pixel models have been shown to use those attributes.

Before:

```text
Metadata AUROC 1.0000 exposes an available shortcut.
```

After:

```text
Metadata-only AUROC 1.0000 shows perfect ranking from technical attributes.
```

## 20. T8 plain Results wording

Reason: Definition is supplied in Methods; avoid repeated jargon.

Before:

```text
These percentile intervals condition on frozen fits and thresholds;
```

After:

```text
These intervals retain the fitted models and thresholds;
```

## 21. T13 Fig7 interpretation

Reason: Match the simplified heatmap exactly.

Before:

```text
Asterisks indicate at least one exploratory constituent pass, not a confirmed family discovery.
```

After:

```text
Every family contains an exploratory constituent pass; redundant asterisks are omitted, and no family-level test or confirmation is implied.
```

## 22. T8/T9 Results clarity

Reason: Name the gate and explain its concrete failure.

Before:

```text
The 542 raw-rule passes among 1,040 tests fail confirmatory eligibility because Step 5 lacks subjects and encoding overlap.
```

After:

```text
The 542 exploratory passes among 1,040 tests cannot be confirmed because the common-support gate (Algorithm~\ref{alg:pipeline}, line 8) lacks verified subjects and encoding overlap.
```

## 23. T3 delivered supplement

Reason: Give the exact filename rather than an undelivered figure reference.

Before:

```text
Supplementary Fig. S1 supplies the six development-selected feature rainclouds/ECDFs;
```

After:

```text
Supplementary Fig. S1, file \texttt{supplementary.pdf}, supplies the six development-selected feature rainclouds/ECDFs;
```

## 24. \subsection{Base-Paper Summary}

Reason: T10 explicit base designation and honest comparison scope.

Before:

```text

Base papers are studies supplying the benchmark, features, bias controls or detection/explanation objectives used here. Table~\ref{tab:t7} includes FIRE, VIB-Net and FakeBench; PixelatedScatter and MisVisFix instead inform interface design (Table~\ref{tab:t1}). The internal matched comparator is FFT-only.


```

After:

```text

The base papers are ArtBrain \cite{p1}, Kim et al. \cite{p2}, B-Free \cite{p3}, SCADET \cite{p4}, SPAI \cite{p5}, FIRE \cite{p6}, VIB-Net \cite{p7}, CoDA \cite{p8}, FakeBench \cite{p12} and SIDWA \cite{p14} (Table~\ref{tab:t7}). The remaining Table~\ref{tab:t1} studies are related work rather than base methods. No base-paper method was reimplemented; FFT-only is the matched internal ablation comparator, limiting external comparisons to source-reported protocols.


```

## 25. T9 mixed-cohort F1

Reason: Read existing cached mixed-cohort metrics; retain the different-population warning.

Before:

```text
and AUROC 0.9220;
```

After:

```text
and AUROC 0.9220/F1 0.8977;
```

## 26. T4/T10 offset duplicate prose

Reason: The reimplementation limitation now appears explicitly in VI-A.

Before:

```text
No additional trained frequency architecture is presented as a faithful reproduction: the existing FFT-only logistic probe remains the matched frequency comparator.
```

After:

```text

```

## 27. T9 Discussion gate reference

Reason: Replace numbering ambiguity without weakening the result.

Before:

```text
The Step 5 gate succeeds as an audit by detecting why that stronger inference is unavailable.
```

After:

```text
The common-support gate (Algorithm~\ref{alg:pipeline}, line 8) identifies why that stronger inference is unavailable.
```

## 28. T11 calibrated Discussion heading

Reason: A measured association is not a proven pixel-shortcut mechanism.

Before:

```text
\subsection{Control-Gate Failure as a Forensic Discovery}
```

After:

```text
\subsection{Common-Support Failure and Technical Source Association}
```

## 29. T11 explicitly untested mechanism

Reason: Separate plausible interpretation from tested evidence.

Before:

```text
Neither a zero true origin effect nor complete causal mediation by JPEG follows from this evidence.
```

After:

```text
Neither a zero true origin effect nor complete causal mediation by JPEG follows from this evidence. One untested hypothesis is that local ordinal patterns respond to JPEG block artifacts, which could contribute to the largest ablation effect; the JPEG-50 result motivates, but does not establish, that mechanism.
```

## 30. T11 bounded G1 verdict

Reason: State what was implemented and what was not evaluated.

Before:

```text
G1 is achieved as implemented auditability and measured fidelity, not proof of human explanation quality.
```

After:

```text
G1 is addressed through implemented diagnostics (auditability and measured fidelity); explanation faithfulness and human usefulness were not tested, and display PCA trustworthiness is 0.6928.
```

## 31. T11 G3 verdict

Reason: Avoid claiming causal use of the shortcut by pixel probes.

Before:

```text
G3 yields a negative forensic audit identifying benchmark leakage;
```

After:

```text
G3 yields a negative validity audit consistent with encoding leakage;
```

## 32. T11 Conclusion

Reason: Retain the negative finding while distinguishing association from use.

Before:

```text
Strong release discrimination coexists with encoding leakage and absent verified subjects,
```

After:

```text
Strong release discrimination coexists with origin-aligned encoding and absent verified subjects,
```

## 33. T1 availability truth

Reason: The remote is empty; no upload is claimed.

Before:

```text
The release includes code/tests, pinned dependencies, frozen split IDs/cohort hash, CSVs, figure generators and exact build commands.
```

After:

```text
The prepared local release contains code/tests, pinned dependencies, frozen split IDs/cohort hash, CSVs, figure generators and build commands; publication awaits the authors' push.
```

## 34. T0/T11 declarations names

Reason: Use exact author spelling and professional responsibility wording.

Before:

```text
The authors are responsible for verifying all sources, numerical results and interpretations and for the final manuscript.
```

After:

```text
Wasil Kayani and Umar Asghar are responsible for verifying the sources, numerical results, interpretations and final manuscript.
```

## 35. T0/T6 university and supervisor

Reason: Define the full university name once and retain author-confirmed supervisor.

Before:

```text
The authors thank Ms. Azka Atiq and FAST-NUCES Islamabad for academic guidance.
```

After:

```text
The authors thank Ms. Azka Atiq and FAST National University of Computer and Emerging Sciences (FAST-NUCES), Islamabad, for academic guidance.
```

## 36. T6/T11 references.bib

Reason: Protect acronym capitalization; normalize manuscript-version notes, surname parsing and ISBN; add verified Springer JPEG-bias paper (published 2025, not event/preprint year 2024).

Before:

```text
@article{p1,
 author={Silva, Ravidu Suien Rammuni and Lotfi, Ahmad and Ihianle, Isibor Kennedy and Shahtahmassebi, Golnaz and Bird, Jordan J.},
 title={ArtBrain: An Explainable End-to-End Toolkit for Classification and Attribution of AI-Generated Art and Style},
 journal={IEEE Trans. Multimedia},
 year={2026},
 doi={10.1109/tmm.2026.3743638},
 pages={1--11},
 note={Evidence: arXiv:2412.01512v1. doi: \url{10.1109/tmm.2026.3743638}}
}

@article{p2,
 author={Kim, Seunghwan and Lee, Byunghwee and Lee, Wonjae},
 title={Investigating the diversity and stylization of contemporary user generated visual arts in the complexity entropy plane},
 journal={Sci. Rep.},
 year={2025},
 doi={10.1038/s41598-025-04448-9},
 volume={15},
 number={1},
 pages={22075},
 note={doi: \url{10.1038/s41598-025-04448-9}}
}

@article{p3,
 author={Guillaro, Fabrizio and Zingarini, Giada and Usman, Ben and Sud, Avneesh and Cozzolino, Davide and Verdoliva, Luisa},
 title={A Bias-Free Training Paradigm for More General AI-generated Image Detection},
 journal={2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2025},
 doi={10.1109/cvpr52734.2025.01741},
 pages={18685--18694},
 note={doi: \url{10.1109/cvpr52734.2025.01741}}
}

@article{p4,
 author={Zhang, Xiaolong and Yu, Zekai and Zhao, Jianqiao},
 title={SCADET: A detection framework for AI-generated artwork integrating dynamic frequency attention and contrastive spectral analysis},
 journal={PLOS One},
 year={2025},
 doi={10.1371/journal.pone.0336328},
 volume={20},
 number={11},
 pages={e0336328},
 note={doi: \url{10.1371/journal.pone.0336328}}
}

@article{p5,
 author={Karageorgiou, Dimitrios and Papadopoulos, Symeon and Kompatsiaris, Ioannis and Gavves, Efstratios},
 title={Any-Resolution AI-Generated Image Detection by Spectral Learning},
 journal={2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2025},
 doi={10.1109/cvpr52734.2025.01743},
 pages={18706--18717},
 note={doi: \url{10.1109/cvpr52734.2025.01743}}
}

@article{p6,
 author={Chu, Beilin and Xu, Xuan and Wang, Xin and Zhang, Yufei and You, Weike and Zhou, Linna},
 title={FIRE: Robust Detection of Diffusion-Generated Images via Frequency-Guided Reconstruction Error},
 journal={2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2025},
 doi={10.1109/cvpr52734.2025.01197},
 pages={12830--12839},
 note={doi: \url{10.1109/cvpr52734.2025.01197}}
}

@article{p7,
 author={Zhang, Haifeng and He, Qinghui and Bi, Xiuli and Li, Weisheng and Liu, Bo and Xiao, Bin},
 title={Towards Universal AI-Generated Image Detection by Variational Information Bottleneck Network},
 journal={2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2025},
 doi={10.1109/cvpr52734.2025.02219},
 pages={23828--23837},
 note={doi: \url{10.1109/cvpr52734.2025.02219}}
}

@article{p8,
 author={Jia, Zexi and Yuan, Zhiqiang and Duan, Xiaoyue and Zhang, Jinchao and Zhou, Jie and Jain, Anil K.},
 title={CoDA: Color Distribution Probing for Efficient and Generalizable AI-Generated Image Detection},
 journal={IEEE Trans. Pattern Anal. Mach. Intell.},
 year={2026},
 doi={10.1109/tpami.2026.3696399},
 volume={48},
 number={10},
 pages={12100--12115},
 note={Evidence: arXiv:2605.24306. doi: \url{10.1109/tpami.2026.3696399}}
}

@article{p9,
 author={Guo, Ziheng and Wei, Tianxiang and Li, Zeyu and Zhang, Lianghao and Li, Sisi and Zhang, Jiawan},
 title={PixelatedScatter: Arbitrary-Level Visual Abstraction for Large-Scale Multiclass Scatterplots},
 journal={IEEE Trans. Vis. Comput. Graph.},
 year={2026},
 doi={10.1109/tvcg.2025.3633908},
 volume={32},
 number={1},
 pages={123--133},
 note={Evidence: collected author manuscript. doi: \url{10.1109/tvcg.2025.3633908}}
}

@article{p10,
 author={Das, Amit Kumar and Mueller, Klaus},
 title={MisVisFix: An Interactive Dashboard for Detecting, Explaining, and Correcting Misleading Visualizations using Large Language Models},
 journal={IEEE Trans. Vis. Comput. Graph.},
 year={2026},
 doi={10.1109/tvcg.2025.3633884},
 volume={32},
 number={1},
 pages={134--144},
 note={Evidence: collected author manuscript. doi: \url{10.1109/tvcg.2025.3633884}}
}

@article{p11,
 author={Kim, Jin and Lee, Byunghwee and You, Taekho and Yun, Jinhyuk},
 title={Context-aware multimodal AI navigates hidden pathways in five centuries of art evolution},
 journal={Proceedings of the National Academy of Sciences},
 year={2026},
 doi={10.1073/pnas.2517969123},
 volume={123},
 number={30},
 pages={e2517969123},
 note={Evidence: arXiv:2503.13531v1. doi: \url{10.1073/pnas.2517969123}}
}

@article{p12,
 author={Li, Yixuan and Liu, Xuelin and Wang, Xiaoyang and Lee, Bu Sung and Wang, Shiqi and Rocha, Anderson and Lin, Weisi},
 title={FakeBench: Probing Explainable Fake Image Detection via Large Multimodal Models},
 journal={IEEE Trans. Inf. Forensics Security},
 year={2025},
 doi={10.1109/tifs.2025.3597211},
 volume={20},
 pages={8730--8745},
 note={Evidence: arXiv:2404.13306v2. doi: \url{10.1109/tifs.2025.3597211}}
}

@article{p13,
 author={Kong, Chenqi and Luo, Anwei and Wang, Shiqi and Li, Haoliang and Rocha, Anderson and Kot, Alex C.},
 title={Pixel-Inconsistency Modeling for Image Manipulation Localization},
 journal={IEEE Trans. Pattern Anal. Mach. Intell.},
 year={2025},
 doi={10.1109/tpami.2025.3541028},
 volume={47},
 number={6},
 pages={4455--4472},
 note={Evidence: arXiv:2310.00234v2. doi: \url{10.1109/tpami.2025.3541028}}
}

@article{p14,
 author={Li, Luo and Lu, Tianyi and Song, Jiaxin and Cheng, Ke},
 title={SIDWA: Synthetic Image Detection Based on Discrete Wavelet Transform Stem and Deformable Sliding Window Cross-Attention},
 journal={Electronics},
 year={2026},
 doi={10.3390/electronics15040891},
 volume={15},
 number={4},
 pages={891},
 note={doi: \url{10.3390/electronics15040891}}
}

@article{p15,
 author={Yikun Ji and Yan Hong and Bowen Deng and Jun Lan and Huijia Zhu and Weiqiang Wang and Liqing Zhang and Jianfu Zhang},
 title={Locate-Then-Examine: Grounded Region Reasoning Improves Detection of AI-Generated Images},
 journal={arXiv:2510.04225v2},
 year={2026},
 doi={10.48550/arXiv.2510.04225},
 note={Publication details unavailable; collected manuscript version. doi: \url{10.48550/arXiv.2510.04225}}
}

@article{p16,
 author={{Wang Yinghua} and {Li Linyan} and {Ma Wenjuan} and {Zhang Yunzhe}},
 title={AI-generated artwork detection using self-distilled transformers with global–local feature learning and Grad-CAM interpretability},
 journal={Sci. Rep.},
 year={2026},
 doi={10.1038/s41598-025-29229-2},
 volume={16},
 number={1},
 pages={497},
 note={doi: \url{10.1038/s41598-025-29229-2}}
}

@article{resnet,
 author={He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
 title={Deep Residual Learning for Image Recognition},
 journal={2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2016},
 doi={10.1109/cvpr.2016.90},
 pages={770--778},
 note={doi: \url{10.1109/cvpr.2016.90}}
}

@article{imagenet,
 author={Russakovsky, Olga and Deng, Jia and Su, Hao and Krause, Jonathan and Satheesh, Sanjeev and Ma, Sean and Huang, Zhiheng and Karpathy, Andrej and Khosla, Aditya and Bernstein, Michael and Berg, Alexander C. and Fei-Fei, Li},
 title={ImageNet Large Scale Visual Recognition Challenge},
 journal={Int. J. Comput. Vis.},
 year={2015},
 doi={10.1007/s11263-015-0816-y},
 volume={115},
 number={3},
 pages={211--252},
 note={doi: \url{10.1007/s11263-015-0816-y}}
}

@article{bandt,
 author={Bandt, Christoph and Pompe, Bernd},
 title={Permutation Entropy: A Natural Complexity Measure for Time Series},
 journal={Phys. Rev. Lett.},
 year={2002},
 doi={10.1103/physrevlett.88.174102},
 volume={88},
 number={17},
 pages={174102},
 note={doi: \url{10.1103/physrevlett.88.174102}}
}

@article{rosso,
 author={Rosso, O. A. and Larrondo, H. A. and Martin, M. T. and Plastino, A. and Fuentes, M. A.},
 title={Distinguishing Noise from Chaos},
 journal={Phys. Rev. Lett.},
 year={2007},
 doi={10.1103/physrevlett.99.154102},
 volume={99},
 number={15},
 pages={154102},
 note={doi: \url{10.1103/physrevlett.99.154102}}
}

@article{venna,
 author={Venna, Jarkko and Kaski, Samuel},
 title={Neighborhood Preservation in Nonlinear Projection Methods: An Experimental Study},
 journal={Lecture Notes in Computer Science},
 year={2001},
 doi={10.1007/3-540-44668-0_68},
 pages={485--491},
 note={doi: \url{10.1007/3-540-44668-0_68}}
}

@article{silhouette,
 author={Rousseeuw, Peter J.},
 title={Silhouettes: A graphical aid to the interpretation and validation of cluster analysis},
 journal={J. Comput. Appl. Math.},
 year={1987},
 doi={10.1016/0377-0427(87)90125-7},
 volume={20},
 pages={53--65},
 note={doi: \url{10.1016/0377-0427(87)90125-7}}
}

@article{bh,
 author={Benjamini, Yoav and Hochberg, Yosef},
 title={Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing},
 journal={Journal of the Royal Statistical Society Series B: Statistical Methodology},
 year={1995},
 doi={10.1111/j.2517-6161.1995.tb02031.x},
 volume={57},
 number={1},
 pages={289--300},
 note={doi: \url{10.1111/j.2517-6161.1995.tb02031.x}}
}

@article{bootstrap,
 author={Efron, B.},
 title={Bootstrap Methods: Another Look at the Jackknife},
 journal={The Annals of Statistics},
 year={1979},
 doi={10.1214/aos/1176344552},
 volume={7},
 number={1},
 pages={1--26},
 note={doi: \url{10.1214/aos/1176344552}}
}

@article{ks,
 author={Massey, Frank J.},
 title={The Kolmogorov-Smirnov Test for Goodness of Fit},
 journal={J. Am. Stat. Assoc.},
 year={1951},
 doi={10.1080/01621459.1951.10500769},
 volume={46},
 number={253},
 pages={68--78},
 note={doi: \url{10.1080/01621459.1951.10500769}}
}

@article{ot,
 author={Peyré, Gabriel and Cuturi, Marco},
 title={Computational Optimal Transport with Applications to Data Sciences},
 journal={Foundations and Trends® in Machine Learning},
 year={2019},
 doi={10.1561/2200000073},
 volume={11},
 number={5-6},
 pages={355--607},
 note={doi: \url{10.1561/2200000073}}
}

@article{numpy,
 author={Harris, Charles R. and Millman, K. Jarrod and van der Walt, Stéfan J. and Gommers, Ralf and Virtanen, Pauli and Cournapeau, David and Wieser, Eric and Taylor, Julian and Berg, Sebastian and Smith, Nathaniel J. and Kern, Robert and Picus, Matti and Hoyer, Stephan and van Kerkwijk, Marten H. and Brett, Matthew and Haldane, Allan and del Río, Jaime Fernández and Wiebe, Mark and Peterson, Pearu and Gérard-Marchant, Pierre and Sheppard, Kevin and Reddy, Tyler and Weckesser, Warren and Abbasi, Hameer and Gohlke, Christoph and Oliphant, Travis E.},
 title={Array programming with NumPy},
 journal={Nature},
 year={2020},
 doi={10.1038/s41586-020-2649-2},
 volume={585},
 number={7825},
 pages={357--362},
 note={doi: \url{10.1038/s41586-020-2649-2}}
}

@article{scipy,
 author={Virtanen, Pauli and Gommers, Ralf and Oliphant, Travis E. and Haberland, Matt and Reddy, Tyler and Cournapeau, David and Burovski, Evgeni and Peterson, Pearu and Weckesser, Warren and Bright, Jonathan and van der Walt, Stéfan J. and Brett, Matthew and Wilson, Joshua and Millman, K. Jarrod and Mayorov, Nikolay and Nelson, Andrew R. J. and Jones, Eric and Kern, Robert and Larson, Eric and Carey, C J and Polat, İlhan and Feng, Yu and Moore, Eric W. and VanderPlas, Jake and Laxalde, Denis and Perktold, Josef and Cimrman, Robert and Henriksen, Ian and Quintero, E. A. and Harris, Charles R. and Archibald, Anne M. and Ribeiro, Antônio H. and Pedregosa, Fabian and van Mulbregt, Paul and Vijaykumar, Aditya and Bardelli, Alessandro Pietro and Rothberg, Alex and Hilboll, Andreas and Kloeckner, Andreas and Scopatz, Anthony and Lee, Antony and Rokem, Ariel and Woods, C. Nathan and Fulton, Chad and Masson, Charles and Häggström, Christian and Fitzgerald, Clark and Nicholson, David A. and Hagen, David R. and Pasechnik, Dmitrii V. and Olivetti, Emanuele and Martin, Eric and Wieser, Eric and Silva, Fabrice and Lenders, Felix and Wilhelm, Florian and Young, G. and Price, Gavin A. and Ingold, Gert-Ludwig and Allen, Gregory E. and Lee, Gregory R. and Audren, Hervé and Probst, Irvin and Dietrich, Jörg P. and Silterra, Jacob and Webber, James T and Slavič, Janko and Nothman, Joel and Buchner, Johannes and Kulick, Johannes and Schönberger, Johannes L. and de Miranda Cardoso, José Vinícius and Reimer, Joscha and Harrington, Joseph and Rodríguez, Juan Luis Cano and Nunez-Iglesias, Juan and Kuczynski, Justin and Tritz, Kevin and Thoma, Martin and Newville, Matthew and Kümmerer, Matthias and Bolingbroke, Maximilian and Tartre, Michael and Pak, Mikhail and Smith, Nathaniel J. and Nowaczyk, Nikolai and Shebanov, Nikolay and Pavlyk, Oleksandr and Brodtkorb, Per A. and Lee, Perry and McGibbon, Robert T. and Feldbauer, Roman and Lewis, Sam and Tygier, Sam and Sievert, Scott and Vigna, Sebastiano and Peterson, Stefan and More, Surhud and Pudlik, Tadeusz and Oshima, Takuya and Pingel, Thomas J. and Robitaille, Thomas P. and Spura, Thomas and Jones, Thouis R. and Cera, Tim and Leslie, Tim and Zito, Tiziano and Krauss, Tom and Upadhyay, Utkarsh and Halchenko, Yaroslav O. and Vázquez-Baeza, Yoshiki},
 title={SciPy 1.0: fundamental algorithms for scientific computing in Python},
 journal={Nature Methods},
 year={2020},
 doi={10.1038/s41592-019-0686-2},
 volume={17},
 number={3},
 pages={261--272},
 note={doi: \url{10.1038/s41592-019-0686-2}}
}

@article{wavelet,
 author={Lee, Gregory and Gommers, Ralf and Waselewski, Filip and Wohlfahrt, Kai and O'Leary, Aaron},
 title={PyWavelets: A Python package for wavelet analysis},
 journal={Journal of Open Source Software},
 year={2019},
 doi={10.21105/joss.01237},
 volume={4},
 number={36},
 pages={1237},
 note={doi: \url{10.21105/joss.01237}}
}

@article{dinov2,
 author={Maxime Oquab and Timothee Darcet and Theo Moutakanni and others},
 title={DINOv2: Learning Robust Visual Features without Supervision},
 journal={Transactions on Machine Learning Research},
 year={2024},
 url={https://openreview.net/forum?id=a68SUt6zFt}
}

@article{sklearn,
 author={Fabian Pedregosa and Gael Varoquaux and Alexandre Gramfort and others},
 title={Scikit-learn: Machine Learning in Python},
 journal={J. Mach. Learn. Res.},
 volume={12},
 number={85},
 pages={2825--2830},
 year={2011},
 url={https://jmlr.org/papers/v12/pedregosa11a.html}
}

@article{tsne,
 author={Laurens van der Maaten and Geoffrey Hinton},
 title={Visualizing Data using t-SNE},
 journal={J. Mach. Learn. Res.},
 volume={9},
 number={86},
 pages={2579--2605},
 year={2008},
 url={https://jmlr.org/papers/v9/vandermaaten08a.html}
}

@article{pytorch,
 author={Adam Paszke and Sam Gross and Francisco Massa and others},
 title={PyTorch: An Imperative Style, High-Performance Deep Learning Library},
 journal={Adv. Neural Inf. Process. Syst.},
 volume={32},
 year={2019},
 url={https://proceedings.neurips.cc/paper_files/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html}
}

@article{artbench,
 author={Peiyuan Liao and Xiuyu Li and Xihui Liu and Kurt Keutzer},
 title={The ArtBench Dataset: Benchmarking Generative Models with Artworks},
 journal={arXiv:2206.11404},
 year={2022},
 doi={10.48550/arXiv.2206.11404},
 note={doi: \url{10.48550/arXiv.2206.11404}}
}

@article{imagehash,
 author={Johannes Buchner},
 title={ImageHash: Perceptual image hashing in Python},
 journal={Software, version 4.3.2},
 year={2025},
 url={https://pypi.org/project/ImageHash/4.3.2/},
 note={Implementation reference for pHash and dHash; software documentation, not an algorithm-origin claim}
}

@book{imaging,
 author={Rafael C. Gonzalez and Richard E. Woods},
 title={Digital Image Processing},
 edition={4},
 publisher={Pearson},
 year={2018},
 note={ISBN 9780133356724},
 url={https://imageprocessingplace.com/}
}

@article{torchvision,
 author={{PyTorch contributors}},
 title={Torchvision ResNet-50: IMAGENET1K V2 weights},
 journal={Torchvision 0.21 documentation},
 year={2025},
 url={https://docs.pytorch.org/vision/0.21/models/generated/torchvision.models.resnet50.html}
}

@IEEEtranBSTCTL{bstctl, CTLuse_forced_etal={yes}, CTLmax_names_forced_etal={3}, CTLnames_show_etal={1}}
```

After:

```text
@article{p1,
 author={Silva, Ravidu Suien Rammuni and Lotfi, Ahmad and Ihianle, Isibor Kennedy and Shahtahmassebi, Golnaz and Bird, Jordan J.},
 title={{ArtBrain: An Explainable End-to-End Toolkit for Classification and Attribution of AI-Generated Art and Style}},
 journal={IEEE Trans. Multimedia},
 year={2026},
 doi={10.1109/tmm.2026.3743638},
 pages={1--11},
 note={Manuscript version read: arXiv:2412.01512v1. doi: \url{10.1109/tmm.2026.3743638}}
}

@article{p2,
 author={Kim, Seunghwan and Lee, Byunghwee and Lee, Wonjae},
 title={{Investigating the diversity and stylization of contemporary user generated visual arts in the complexity entropy plane}},
 journal={Sci. Rep.},
 year={2025},
 doi={10.1038/s41598-025-04448-9},
 volume={15},
 number={1},
 pages={22075},
 note={doi: \url{10.1038/s41598-025-04448-9}}
}

@article{p3,
 author={Guillaro, Fabrizio and Zingarini, Giada and Usman, Ben and Sud, Avneesh and Cozzolino, Davide and Verdoliva, Luisa},
 title={{A Bias-Free Training Paradigm for More General AI-generated Image Detection}},
 journal={2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2025},
 doi={10.1109/cvpr52734.2025.01741},
 pages={18685--18694},
 note={doi: \url{10.1109/cvpr52734.2025.01741}}
}

@article{p4,
 author={Zhang, Xiaolong and Yu, Zekai and Zhao, Jianqiao},
 title={{SCADET: A detection framework for AI-generated artwork integrating dynamic frequency attention and contrastive spectral analysis}},
 journal={PLOS One},
 year={2025},
 doi={10.1371/journal.pone.0336328},
 volume={20},
 number={11},
 pages={e0336328},
 note={doi: \url{10.1371/journal.pone.0336328}}
}

@article{p5,
 author={Karageorgiou, Dimitrios and Papadopoulos, Symeon and Kompatsiaris, Ioannis and Gavves, Efstratios},
 title={{Any-Resolution AI-Generated Image Detection by Spectral Learning}},
 journal={2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2025},
 doi={10.1109/cvpr52734.2025.01743},
 pages={18706--18717},
 note={doi: \url{10.1109/cvpr52734.2025.01743}}
}

@article{p6,
 author={Chu, Beilin and Xu, Xuan and Wang, Xin and Zhang, Yufei and You, Weike and Zhou, Linna},
 title={{FIRE: Robust Detection of Diffusion-Generated Images via Frequency-Guided Reconstruction Error}},
 journal={2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2025},
 doi={10.1109/cvpr52734.2025.01197},
 pages={12830--12839},
 note={doi: \url{10.1109/cvpr52734.2025.01197}}
}

@article{p7,
 author={Zhang, Haifeng and He, Qinghui and Bi, Xiuli and Li, Weisheng and Liu, Bo and Xiao, Bin},
 title={{Towards Universal AI-Generated Image Detection by Variational Information Bottleneck Network}},
 journal={2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2025},
 doi={10.1109/cvpr52734.2025.02219},
 pages={23828--23837},
 note={doi: \url{10.1109/cvpr52734.2025.02219}}
}

@article{p8,
 author={Jia, Zexi and Yuan, Zhiqiang and Duan, Xiaoyue and Zhang, Jinchao and Zhou, Jie and Jain, Anil K.},
 title={{CoDA: Color Distribution Probing for Efficient and Generalizable AI-Generated Image Detection}},
 journal={IEEE Trans. Pattern Anal. Mach. Intell.},
 year={2026},
 doi={10.1109/tpami.2026.3696399},
 volume={48},
 number={10},
 pages={12100--12115},
 note={Manuscript version read: arXiv:2605.24306. doi: \url{10.1109/tpami.2026.3696399}}
}

@article{p9,
 author={Guo, Ziheng and Wei, Tianxiang and Li, Zeyu and Zhang, Lianghao and Li, Sisi and Zhang, Jiawan},
 title={{PixelatedScatter: Arbitrary-Level Visual Abstraction for Large-Scale Multiclass Scatterplots}},
 journal={IEEE Trans. Vis. Comput. Graph.},
 year={2026},
 doi={10.1109/tvcg.2025.3633908},
 volume={32},
 number={1},
 pages={123--133},
 note={Manuscript version read: collected author manuscript. doi: \url{10.1109/tvcg.2025.3633908}}
}

@article{p10,
 author={Das, Amit Kumar and Mueller, Klaus},
 title={{MisVisFix: An Interactive Dashboard for Detecting, Explaining, and Correcting Misleading Visualizations using Large Language Models}},
 journal={IEEE Trans. Vis. Comput. Graph.},
 year={2026},
 doi={10.1109/tvcg.2025.3633884},
 volume={32},
 number={1},
 pages={134--144},
 note={Manuscript version read: collected author manuscript. doi: \url{10.1109/tvcg.2025.3633884}}
}

@article{p11,
 author={Kim, Jin and Lee, Byunghwee and You, Taekho and Yun, Jinhyuk},
 title={{Context-aware multimodal AI navigates hidden pathways in five centuries of art evolution}},
 journal={Proceedings of the National Academy of Sciences},
 year={2026},
 doi={10.1073/pnas.2517969123},
 volume={123},
 number={30},
 pages={e2517969123},
 note={Manuscript version read: arXiv:2503.13531v1. doi: \url{10.1073/pnas.2517969123}}
}

@article{p12,
 author={Li, Yixuan and Liu, Xuelin and Wang, Xiaoyang and Lee, Bu Sung and Wang, Shiqi and Rocha, Anderson and Lin, Weisi},
 title={{FakeBench: Probing Explainable Fake Image Detection via Large Multimodal Models}},
 journal={IEEE Trans. Inf. Forensics Security},
 year={2025},
 doi={10.1109/tifs.2025.3597211},
 volume={20},
 pages={8730--8745},
 note={Manuscript version read: arXiv:2404.13306v2. doi: \url{10.1109/tifs.2025.3597211}}
}

@article{p13,
 author={Kong, Chenqi and Luo, Anwei and Wang, Shiqi and Li, Haoliang and Rocha, Anderson and Kot, Alex C.},
 title={{Pixel-Inconsistency Modeling for Image Manipulation Localization}},
 journal={IEEE Trans. Pattern Anal. Mach. Intell.},
 year={2025},
 doi={10.1109/tpami.2025.3541028},
 volume={47},
 number={6},
 pages={4455--4472},
 note={Manuscript version read: arXiv:2310.00234v2. doi: \url{10.1109/tpami.2025.3541028}}
}

@article{p14,
 author={Li, Luo and Lu, Tianyi and Song, Jiaxin and Cheng, Ke},
 title={{SIDWA: Synthetic Image Detection Based on Discrete Wavelet Transform Stem and Deformable Sliding Window Cross-Attention}},
 journal={Electronics},
 year={2026},
 doi={10.3390/electronics15040891},
 volume={15},
 number={4},
 pages={891},
 note={doi: \url{10.3390/electronics15040891}}
}

@article{p15,
 author={Yikun Ji and Yan Hong and Bowen Deng and Jun Lan and Huijia Zhu and Weiqiang Wang and Liqing Zhang and Jianfu Zhang},
 title={{Locate-Then-Examine: Grounded Region Reasoning Improves Detection of AI-Generated Images}},
 journal={arXiv:2510.04225v2},
 year={2026},
 doi={10.48550/arXiv.2510.04225},
 note={Publication details unavailable; collected manuscript version. doi: \url{10.48550/arXiv.2510.04225}}
}

@article{p16,
 author={Wang, Yinghua and Li, Linyan and Ma, Wenjuan and Zhang, Yunzhe},
 title={{AI-generated artwork detection using self-distilled transformers with global–local feature learning and Grad-CAM interpretability}},
 journal={Sci. Rep.},
 year={2026},
 doi={10.1038/s41598-025-29229-2},
 volume={16},
 number={1},
 pages={497},
 note={doi: \url{10.1038/s41598-025-29229-2}}
}

@article{resnet,
 author={He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
 title={{Deep Residual Learning for Image Recognition}},
 journal={2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
 year={2016},
 doi={10.1109/cvpr.2016.90},
 pages={770--778},
 note={doi: \url{10.1109/cvpr.2016.90}}
}

@article{imagenet,
 author={Russakovsky, Olga and Deng, Jia and Su, Hao and Krause, Jonathan and Satheesh, Sanjeev and Ma, Sean and Huang, Zhiheng and Karpathy, Andrej and Khosla, Aditya and Bernstein, Michael and Berg, Alexander C. and Fei-Fei, Li},
 title={{ImageNet Large Scale Visual Recognition Challenge}},
 journal={Int. J. Comput. Vis.},
 year={2015},
 doi={10.1007/s11263-015-0816-y},
 volume={115},
 number={3},
 pages={211--252},
 note={doi: \url{10.1007/s11263-015-0816-y}}
}

@article{bandt,
 author={Bandt, Christoph and Pompe, Bernd},
 title={{Permutation Entropy: A Natural Complexity Measure for Time Series}},
 journal={Phys. Rev. Lett.},
 year={2002},
 doi={10.1103/physrevlett.88.174102},
 volume={88},
 number={17},
 pages={174102},
 note={doi: \url{10.1103/physrevlett.88.174102}}
}

@article{rosso,
 author={Rosso, O. A. and Larrondo, H. A. and Martin, M. T. and Plastino, A. and Fuentes, M. A.},
 title={{Distinguishing Noise from Chaos}},
 journal={Phys. Rev. Lett.},
 year={2007},
 doi={10.1103/physrevlett.99.154102},
 volume={99},
 number={15},
 pages={154102},
 note={doi: \url{10.1103/physrevlett.99.154102}}
}

@article{venna,
 author={Venna, Jarkko and Kaski, Samuel},
 title={{Neighborhood Preservation in Nonlinear Projection Methods: An Experimental Study}},
 journal={Lecture Notes in Computer Science},
 year={2001},
 doi={10.1007/3-540-44668-0_68},
 pages={485--491},
 note={doi: \url{10.1007/3-540-44668-0_68}}
}

@article{silhouette,
 author={Rousseeuw, Peter J.},
 title={{Silhouettes: A graphical aid to the interpretation and validation of cluster analysis}},
 journal={J. Comput. Appl. Math.},
 year={1987},
 doi={10.1016/0377-0427(87)90125-7},
 volume={20},
 pages={53--65},
 note={doi: \url{10.1016/0377-0427(87)90125-7}}
}

@article{bh,
 author={Benjamini, Yoav and Hochberg, Yosef},
 title={{Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing}},
 journal={Journal of the Royal Statistical Society Series B: Statistical Methodology},
 year={1995},
 doi={10.1111/j.2517-6161.1995.tb02031.x},
 volume={57},
 number={1},
 pages={289--300},
 note={doi: \url{10.1111/j.2517-6161.1995.tb02031.x}}
}

@article{bootstrap,
 author={Efron, B.},
 title={{Bootstrap Methods: Another Look at the Jackknife}},
 journal={The Annals of Statistics},
 year={1979},
 doi={10.1214/aos/1176344552},
 volume={7},
 number={1},
 pages={1--26},
 note={doi: \url{10.1214/aos/1176344552}}
}

@article{ks,
 author={Massey, Frank J.},
 title={{The Kolmogorov-Smirnov Test for Goodness of Fit}},
 journal={J. Am. Stat. Assoc.},
 year={1951},
 doi={10.1080/01621459.1951.10500769},
 volume={46},
 number={253},
 pages={68--78},
 note={doi: \url{10.1080/01621459.1951.10500769}}
}

@article{ot,
 author={Peyré, Gabriel and Cuturi, Marco},
 title={{Computational Optimal Transport with Applications to Data Sciences}},
 journal={Foundations and Trends® in Machine Learning},
 year={2019},
 doi={10.1561/2200000073},
 volume={11},
 number={5-6},
 pages={355--607},
 note={doi: \url{10.1561/2200000073}}
}

@article{numpy,
 author={Harris, Charles R. and Millman, K. Jarrod and van der Walt, Stéfan J. and Gommers, Ralf and Virtanen, Pauli and Cournapeau, David and Wieser, Eric and Taylor, Julian and Berg, Sebastian and Smith, Nathaniel J. and Kern, Robert and Picus, Matti and Hoyer, Stephan and van Kerkwijk, Marten H. and Brett, Matthew and Haldane, Allan and del Río, Jaime Fernández and Wiebe, Mark and Peterson, Pearu and Gérard-Marchant, Pierre and Sheppard, Kevin and Reddy, Tyler and Weckesser, Warren and Abbasi, Hameer and Gohlke, Christoph and Oliphant, Travis E.},
 title={{Array programming with NumPy}},
 journal={Nature},
 year={2020},
 doi={10.1038/s41586-020-2649-2},
 volume={585},
 number={7825},
 pages={357--362},
 note={doi: \url{10.1038/s41586-020-2649-2}}
}

@article{scipy,
 author={Virtanen, Pauli and Gommers, Ralf and Oliphant, Travis E. and Haberland, Matt and Reddy, Tyler and Cournapeau, David and Burovski, Evgeni and Peterson, Pearu and Weckesser, Warren and Bright, Jonathan and van der Walt, Stéfan J. and Brett, Matthew and Wilson, Joshua and Millman, K. Jarrod and Mayorov, Nikolay and Nelson, Andrew R. J. and Jones, Eric and Kern, Robert and Larson, Eric and Carey, C J and Polat, İlhan and Feng, Yu and Moore, Eric W. and VanderPlas, Jake and Laxalde, Denis and Perktold, Josef and Cimrman, Robert and Henriksen, Ian and Quintero, E. A. and Harris, Charles R. and Archibald, Anne M. and Ribeiro, Antônio H. and Pedregosa, Fabian and van Mulbregt, Paul and Vijaykumar, Aditya and Bardelli, Alessandro Pietro and Rothberg, Alex and Hilboll, Andreas and Kloeckner, Andreas and Scopatz, Anthony and Lee, Antony and Rokem, Ariel and Woods, C. Nathan and Fulton, Chad and Masson, Charles and Häggström, Christian and Fitzgerald, Clark and Nicholson, David A. and Hagen, David R. and Pasechnik, Dmitrii V. and Olivetti, Emanuele and Martin, Eric and Wieser, Eric and Silva, Fabrice and Lenders, Felix and Wilhelm, Florian and Young, G. and Price, Gavin A. and Ingold, Gert-Ludwig and Allen, Gregory E. and Lee, Gregory R. and Audren, Hervé and Probst, Irvin and Dietrich, Jörg P. and Silterra, Jacob and Webber, James T and Slavič, Janko and Nothman, Joel and Buchner, Johannes and Kulick, Johannes and Schönberger, Johannes L. and de Miranda Cardoso, José Vinícius and Reimer, Joscha and Harrington, Joseph and Rodríguez, Juan Luis Cano and Nunez-Iglesias, Juan and Kuczynski, Justin and Tritz, Kevin and Thoma, Martin and Newville, Matthew and Kümmerer, Matthias and Bolingbroke, Maximilian and Tartre, Michael and Pak, Mikhail and Smith, Nathaniel J. and Nowaczyk, Nikolai and Shebanov, Nikolay and Pavlyk, Oleksandr and Brodtkorb, Per A. and Lee, Perry and McGibbon, Robert T. and Feldbauer, Roman and Lewis, Sam and Tygier, Sam and Sievert, Scott and Vigna, Sebastiano and Peterson, Stefan and More, Surhud and Pudlik, Tadeusz and Oshima, Takuya and Pingel, Thomas J. and Robitaille, Thomas P. and Spura, Thomas and Jones, Thouis R. and Cera, Tim and Leslie, Tim and Zito, Tiziano and Krauss, Tom and Upadhyay, Utkarsh and Halchenko, Yaroslav O. and Vázquez-Baeza, Yoshiki},
 title={{SciPy 1.0: fundamental algorithms for scientific computing in Python}},
 journal={Nature Methods},
 year={2020},
 doi={10.1038/s41592-019-0686-2},
 volume={17},
 number={3},
 pages={261--272},
 note={doi: \url{10.1038/s41592-019-0686-2}}
}

@article{wavelet,
 author={Lee, Gregory and Gommers, Ralf and Waselewski, Filip and Wohlfahrt, Kai and O'Leary, Aaron},
 title={{PyWavelets: A Python package for wavelet analysis}},
 journal={Journal of Open Source Software},
 year={2019},
 doi={10.21105/joss.01237},
 volume={4},
 number={36},
 pages={1237},
 note={doi: \url{10.21105/joss.01237}}
}

@article{dinov2,
 author={Maxime Oquab and Timothee Darcet and Theo Moutakanni and others},
 title={{DINOv2: Learning Robust Visual Features without Supervision}},
 journal={Transactions on Machine Learning Research},
 year={2024},
 url={https://openreview.net/forum?id=a68SUt6zFt}
}

@article{sklearn,
 author={Fabian Pedregosa and Gael Varoquaux and Alexandre Gramfort and others},
 title={{Scikit-learn: Machine Learning in Python}},
 journal={J. Mach. Learn. Res.},
 volume={12},
 number={85},
 pages={2825--2830},
 year={2011},
 url={https://jmlr.org/papers/v12/pedregosa11a.html}
}

@article{tsne,
 author={Laurens van der Maaten and Geoffrey Hinton},
 title={{Visualizing Data using t-SNE}},
 journal={J. Mach. Learn. Res.},
 volume={9},
 number={86},
 pages={2579--2605},
 year={2008},
 url={https://jmlr.org/papers/v9/vandermaaten08a.html}
}

@article{pytorch,
 author={Adam Paszke and Sam Gross and Francisco Massa and others},
 title={{PyTorch: An Imperative Style, High-Performance Deep Learning Library}},
 journal={Adv. Neural Inf. Process. Syst.},
 volume={32},
 year={2019},
 url={https://proceedings.neurips.cc/paper_files/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html}
}

@article{artbench,
 author={Peiyuan Liao and Xiuyu Li and Xihui Liu and Kurt Keutzer},
 title={{The ArtBench Dataset: Benchmarking Generative Models with Artworks}},
 journal={arXiv:2206.11404},
 year={2022},
 doi={10.48550/arXiv.2206.11404},
 note={doi: \url{10.48550/arXiv.2206.11404}}
}

@article{imagehash,
 author={Johannes Buchner},
 title={{ImageHash: Perceptual image hashing in Python}},
 journal={Software, version 4.3.2},
 year={2025},
 url={https://pypi.org/project/ImageHash/4.3.2/},
 note={Implementation reference for pHash and dHash; software documentation, not an algorithm-origin claim}
}

@book{imaging,
 author={Rafael C. Gonzalez and Richard E. Woods},
 title={{Digital Image Processing}},
 edition={4},
 publisher={Pearson},
 year={2018},
 note={{ISBN} 9780133356724},
 url={https://imageprocessingplace.com/}
}

@article{torchvision,
 author={{PyTorch contributors}},
 title={{Torchvision ResNet-50: IMAGENET1K V2 weights}},
 journal={Torchvision 0.21 documentation},
 year={2025},
 url={https://docs.pytorch.org/vision/0.21/models/generated/torchvision.models.resnet50.html}
}

@IEEEtranBSTCTL{bstctl, CTLuse_forced_etal={yes}, CTLmax_names_forced_etal={3}, CTLnames_show_etal={1}}
@inproceedings{jpeg_bias,
 author={Grommelt, Patrick and Weiss, Louis and Pfreundt, Franz-Josef and Keuper, Janis},
 title={{Fake or JPEG? Revealing Common Biases in Generated Image Detection Datasets}},
 booktitle={Computer Vision -- ECCV 2024 Workshops},
 series={Lecture Notes in Computer Science},
 volume={15644},
 pages={80--95},
 publisher={Springer},
 year={2025},
 doi={10.1007/978-3-031-92089-9_6},
 note={Manuscript version read: arXiv:2403.17608v2. doi: \url{10.1007/978-3-031-92089-9_6}}
}

```

## 37. T5/T10 derived_improvements.tex

Reason: Lead with strongest baselines; relative deltas derive from unrounded saved metrics, not rounded paper values.

Before:

```text
The matched handcrafted-minus-FFT differences, computed before rounding, are 0.298514 AUROC (43.6487\% relative to FFT-only) and 0.259029 F1 (37.9268\% relative). Thus the displayed gains are +0.2985 AUROC (+43.65\%) and +0.2590 F1 (+37.93\%). The denominator for each relative gain is the corresponding FFT-only score; the latter differs from a percentage computed using already rounded table entries.
```

After:

```text
The handcrafted probe first trails the strongest matched baseline, ResNet-50, by -0.0175 AUROC (-1.75\%; 95\% interval $[-0.0216,-0.0140]$), and DINOv2 by -0.0173 (-1.73\%). Relative differences divide the unrounded score difference by the comparator's AUROC. Against FFT-only, the internal ablation comparator, the gain is +0.2985 AUROC (+43.65\%) and +0.2590 F1 (+37.93\%); each denominator is the corresponding FFT-only score.

```

## Space offset 1: \subsection{Held-Out Probe Evaluation}

T8 remove repeated evaluation setup; preserve the predictive hierarchy, calibration distinction and correct ARI scope.

Before:

```text

Tables~\ref{tab:t4} and \ref{tab:essential} report primary metrics and validation-selected settings; Fig.~\ref{fig:f3} combines ROC/PR curves, per-style scores with 1,000-group-bootstrap 95\% intervals and the clustering cross-check. Handcrafted AUROC is 0.9824, and is outperformed by ResNet-50 (0.9999) and DINOv2 (0.9997). Metadata-only AUROC 1.0000 shows perfect ranking from technical attributes. Its ECE 0.1940 also shows that perfect ranking need not imply well-calibrated probabilities. Near-zero unlabeled ARI in full standardized/PCA spaces (maximum 0.0034 after rounding) coexists with supervised separation: a fitted decision rule need not reveal two natural clusters. Neither establishes attribution.

```

After:

```text

Tables~\ref{tab:t4}--\ref{tab:seeds} and Fig.~\ref{fig:f3} compare the same primary test identities. ResNet-50 (0.9999) and DINOv2 (0.9997) outperform handcrafted AUROC 0.9824. Metadata-only achieves AUROC 1.0000, yet ECE 0.1940 shows that perfect ranking need not imply calibration. Full standardized/PCA unlabeled ARI remains near zero (maximum 0.0034): supervised ranking need not reveal natural origin clusters.

```


## Space offset 2: V-A paired/repartition paragraph

Keep resampling scope and all tuning limitations without restating Methods.

Before:

```text

Table~\ref{tab:paired} gives paired AUROC-difference intervals using the same 1,000 origin-stratified source-group draws for every probe. These intervals retain the fitted models and thresholds; exclusion of zero concerns predictive ranking on this release, not origin attribution. Table~\ref{tab:seeds} reports five new grouped repartitions of the same fixed cohort (seeds 43--47), retuning all five probes within each development/validation partition. Cached embeddings are reused. Feature-extraction thresholds remain fixed from the original seed-42 development set; only preprocessing and probes are refitted. Thus these are conditional split-sensitivity runs, not full pipeline replications.

```

After:

```text

Paired intervals in Table~\ref{tab:paired} use identical origin-stratified group draws and concern predictive ranking, not attribution. Table~\ref{tab:seeds} repartitions the same cohort at seeds 43--47 and refits preprocessing, regularization and thresholds. Cached embeddings and original seed-42 extraction calibration remain fixed; these are conditional split sensitivities, not full pipeline replications.

```


## Space offset 3: \subsection{Entropy--Complexity Atlas and Projection Fidelity}

T8 retain interpretation and dependence limit; formal-descriptor caveat is defined elsewhere.

Before:

```text

The ten-movement atlas in Fig.~\ref{fig:f4} displays shared axes, signed centroid displacements and 500-group-bootstrap Gaussian 95\% ellipses. Most LD clouds occupy lower entropy and higher complexity than Human clouds, but magnitudes differ across styles; the arrows remain descriptive. Equal artwork counts need not imply equal group precision; formal coordinates do not measure aesthetic quality.

```

After:

```text

Figure~\ref{fig:f4} compares shared-axis centroids and distributions. Most LD clouds have lower entropy and higher complexity than Human clouds, with heterogeneous descriptive magnitudes. Equal artwork counts do not imply equal source-group precision.

```


## Space offset 4: V-B projection paragraph

Retain every reported fidelity value and seed scope; initialization/iteration settings remain in Appendix A.

Before:

```text

Two-dimensional PCA explains 93.57\% of development variance yet attains $T(15)=0.6928$ and continuity 0.7571 (Table~\ref{tab:t5}). Three dimensions raise these to 0.7800 and 0.8869. Fifteen t-SNE \cite{tsne} runs span seeds 42--46 and perplexities 15, 30 and 50; trustworthiness ranges 0.9101--0.9185. Figure~\ref{fig:f5} fixes the display at perplexity 30, seed 42, random initialization and 1,000 iterations, without selecting the strongest test-separated embedding. Seed ranges describe algorithmic sensitivity, not inferential confidence intervals. Distance inference remains in standardized features or fixed PCA.

```

After:

```text

PCA2 explains 93.57\% of development variance but attains $T(15)=0.6928$ and $C(15)=0.7571$; PCA3 reaches 0.7800/0.8869 (Table~\ref{tab:t5}). Fifteen t-SNE runs cover seeds 42--46 and perplexities 15/30/50, with trustworthiness 0.9101--0.9185. Figure~\ref{fig:f5} fixes perplexity 30/seed 42 without selecting test separation. Seed ranges measure algorithmic sensitivity; distance inference stays in standardized features or fixed PCA.

```


## Space offset 5: \subsection{Quantitative Side-by-Side Evaluation}

T10/T9 preserve mixed-cohort metrics and comparison limits without repeating the reimplementation disclaimer.

Before:

```text

Table~\ref{tab:t8} marks original-paper quantities with an asterisk. Unstarred primary probes are implemented logistic evaluations on the same frozen split; none is a reproduction of SCADET, SPAI or B-Free. The mixed 45,000-image experiment has a 9,000-image Human-versus-LD+SD test and AUROC 0.9220/F1 0.8977; its different class/source composition prevents a paired resolution-only interpretation. Original paper endpoints that are not AUROC/F1 remain labeled separately rather than substituted into those columns.

```

After:

```text

Table~\ref{tab:t8} distinguishes executed probes from starred source-reported scores. The mixed-cohort 9,000-image test yields AUROC 0.9220/F1 0.8977; its different class/source composition cannot isolate resolution effects. Incompatible endpoints retain their original metric labels.

```


## Space offset 6: \subsection{Fairness and Limitations}

T10 retain concrete fairness differences while removing repeated metadata and incompatible-endpoint warnings.

Before:

```text

SCADET reports a 7:1:2 split rather than the present grouped 60:20:20 split; its release-level processing includes native-$768^2$ SD images resized to $256^2$. The available evidence does not establish equivalent source-group protection. ArtBrain reports joint source/style F1 0.869* and attribution accuracy 0.999*, and its training description reuses test as validation. B-Free's 99.0\%* AUC comes from end-to-end content-aligned photographic training rather than frozen artwork probing. CoDA and VIB-Net use AP endpoints; visualization user-task metrics have no meaningful detector-score delta. The JPEG audit demonstrates a perfect metadata shortcut on this release but does not identify its causal share in any pixel model. Thus the table deliberately does not rank incompatible studies, and available paper versions are stated in the reference crosswalk.


```

After:

```text

SCADET uses 7:1:2 rather than grouped 60:20:20 splitting and includes resized native-$768^2$ SD; equivalent source-group protection is unverified. ArtBrain's joint F1 0.869*/attribution accuracy 0.999* use different targets, and its training description reuses test as validation. B-Free's 99.0\%* AUROC uses end-to-end content-aligned photographic training, not frozen artwork probing. These differences preclude a matched external leaderboard.


```


## Space offset 7: \subsection{Common-Support Failure and Technical Source Association}

T8/T11 remove repeated definitions while retaining every negative/forensic qualification and the explicitly untested hypothesis.

Before:

```text

ResNet-50 and DINOv2 outperform the handcrafted probe in ranking. High AUROC and zero confirmed effects answer different questions. The probe ranks observed release labels; attribution asks whether contrasts persist independently of subjects and processing. The common-support gate (Algorithm~\ref{alg:pipeline}, line 8) identifies why that stronger inference is unavailable. Origin-aligned JPEG quantization and unverified subjects invalidate interpreting the 542 raw passes as confirmed diffusion-origin effects. They do not erase those reproducible associations.

Whole-group permutations preserve recorded families, not the unobserved balance needed for exchangeability. Benjamini--Hochberg controls multiplicity under an appropriate testing model; it cannot remove confounding. Bootstrap intervals quantify conditional uncertainty but cannot manufacture common support. Zero of 1,040 comparisons is confirmed because none is eligible, not because each null has been accepted. Neither a zero true origin effect nor complete causal mediation by JPEG follows from this evidence. One untested hypothesis is that local ordinal patterns respond to JPEG block artifacts, which could contribute to the largest ablation effect; the JPEG-50 result motivates, but does not establish, that mechanism.


```

After:

```text

ResNet-50 and DINOv2 outperform the handcrafted probe, but ranking release labels differs from attributing differences independently of subjects and processing. The common-support gate (Algorithm~\ref{alg:pipeline}, line 8) blocks that stronger inference: origin-aligned JPEG quantization and unverified subjects invalidate interpreting 542 exploratory passes as confirmed diffusion-origin effects, without erasing their descriptive associations.

Whole-group permutations preserve recorded families, not verified exchangeability. Multiplicity adjustment and frozen-fit bootstrap intervals cannot remove confounding or create common support. Zero of 1,040 comparisons is confirmed because none is eligible, not because each null is accepted; neither zero true effects nor complete JPEG mediation follows. An untested hypothesis is that ordinal patterns respond to JPEG blocks and thereby contribute to the largest ablation effect; JPEG-50 sensitivity motivates, but does not establish, this mechanism.


```


## Space offset 8: VIII-B border paragraph

Keep counts/reversals and validity effect; exact border thresholds remain in the named released script.

Before:

```text

Development-quantile low-saturation, low-edge and high-frequency proxies complement a fixed border heuristic. The latter flags an outer eight-pixel luminance strip with standard deviation below 0.025 and adjacent-strip mean jump above 0.08. It flags 369 artworks; 76 lose every quadrant. Comparing both conditions on the identical 5,924 supported artworks yields 12 signed-shift reversals and 23 exploratory-rule reversals, with zero confirmed reversals. This exposes support sensitivity without repairing subject or encoding controls. Overlapping-trigger error-rate gaps and group intervals are supplied in released \texttt{failure\_trigger\_associations.csv}.


```

After:

```text

Development-defined saturation/edge/frequency proxies complement a fixed border heuristic (released \texttt{src/border\_analysis.py}). It flags 369 artworks; 76 lose every quadrant. The identical 5,924 supported artworks yield 12 signed-shift and 23 exploratory-rule reversals, with zero confirmed reversals. Support sensitivity does not repair subject/encoding controls. Overlapping-trigger error gaps and group intervals are in \texttt{failure\_trigger\_associations.csv}.


```


## Space offset 9: \section{Conclusion and Future Work}

T8 remove repeated contribution inventory; preserve negative conclusion, stronger baselines and realistic future controls.

Before:

```text

The study combines transparent feature measurements, grouped held-out probes, neighborhood diagnostics and artwork-linked evidence within a mandatory control-gate workflow. Strong release discrimination coexists with origin-aligned encoding and absent verified subjects, so style-conditioned shifts remain descriptive. Frozen ResNet-50 and DINOv2 outperform the handcrafted probe, but none establishes encoding-independent attribution. The contribution is an inspectable atlas and an explicit account of the inference the benchmark cannot support. Future work should capture lossless museum and diffusion originals with common encoding support, verified subject/prompt links and prespecified processing, then evaluate leave-artist, leave-style and unseen-generator holdouts. Dashboard usefulness and material-specific analyses require independent annotations and human evaluation.


```

After:

```text

The control-gated workflow joins named features, grouped probes, projection diagnostics and linked artwork evidence. Strong release prediction coexists with origin-aligned encoding and unverified subjects; within-style shifts remain descriptive. Frozen ResNet-50 and DINOv2 outperform the handcrafted probe, but none establishes encoding-independent attribution. Future work requires common-encoding originals, verified subject/prompt links and separate artist/style/generator holdouts. Independent annotations and human evaluation are needed to test material-specific explanations and dashboard usefulness.


```


## Final space offset 1: I research question and gaps

Offset additions with duplicated prose; no type/margin reduction or empirical-result change.

Before:

```text
The research question is whether human and diffusion artworks within the same AI-ArtBench style differ in named ordinal, frequency and color measurements after subject, native-dimension and file-encoding controls. Three linked gaps organize the study. \textbf{G1} concerns explainable visual analytics and projection fidelity versus opaque learned features. \textbf{G2} concerns style-conditional human--diffusion feature drift across movements. \textbf{G3} asks whether separation survives subject, native-dimension and encoding controls. The planned temporal question was refined to within-style distribution differences. Neither movement labels nor the present measurements establish a temporal trajectory or aesthetic intention.
```

After:

```text
Within each AI-ArtBench style, the question is which human--diffusion measurement differences survive subject, native-size and encoding controls. \textbf{G1} concerns inspectable diagnostics and projection fidelity; \textbf{G2}, within-style distribution differences; and \textbf{G3}, survival under verified controls. The temporal question was refined before execution: movement labels do not establish chronology or aesthetic intention.
```


## Final space offset 2: I remove duplicated superiority disclaimer

Offset additions with duplicated prose; no type/margin reduction or empirical-result change.

Before:

```text
ArtBrain supplies the artwork benchmark \cite{p1}, and complexity--entropy analysis supplies inspectable formal coordinates \cite{p2}. The proposed contribution joins measurement, prediction and validity auditing, rather than claiming a stronger detector than frozen learned representations.
```

After:

```text
ArtBrain supplies the artwork benchmark \cite{p1}; complexity--entropy analysis supplies inspectable formal coordinates \cite{p2}.
```


## Final space offset 3: III-C equivalent executed objective, define N_d and remove auxiliary C_avg

Offset additions with duplicated prose; no type/margin reduction or empirical-result change.

Before:

```text

For standardized feature $\tilde x_i$, coefficients $w$, unpenalized intercept $b$ and sigmoid $\sigma(z)=(1+e^{-z})^{-1}$, the nominal averaged binary cross-entropy objective is
\begin{align}
\mathcal{L}(w,b)&=-\frac{1}{N_d}\sum_{i=1}^{N_d}\{y_i\log\sigma_i+(1-y_i)\log(1-\sigma_i)\}\nonumber\\
&\quad+\frac{\|w\|_2^2}{2C_{\mathrm{avg}}},\quad \sigma_i=\sigma(w^\top\tilde x_i+b).
\end{align}
The executed unweighted scikit-learn \cite{sklearn} L-BFGS fit uses $C_{\mathrm{avg}}=N_d C_{\mathrm{solver}}$. Thus the averaged-loss penalty is $\|w\|^2/(2N_d C_{\mathrm{solver}})$; tabulated $C$ values are solver values. This preserves the executed regularization scale.


```

After:

```text

For development-standardized feature $\tilde x_i$, coefficients $w$, unpenalized intercept $b$ and $N_d$ development artworks, let $\sigma_i=(1+e^{-(w^\top\tilde x_i+b)})^{-1}$. The executed unweighted scikit-learn \cite{sklearn} L-BFGS objective is
\begin{align}
\mathcal L(w,b)&=-\frac{1}{N_d}\sum_{i=1}^{N_d}\{y_i\log\sigma_i+(1-y_i)\log(1-\sigma_i)\}\nonumber\\
&\quad+\frac{\|w\|_2^2}{2N_d C_{\mathrm{solver}}}.
\end{align}
Thus tabulated $C$ values retain the executed solver scale, rather than an unadjusted averaged-loss penalty.


```


## Final space offset 4: IV-A preserve all audit/split facts concisely

Offset additions with duplicated prose; no type/margin reduction or empirical-result change.

Before:

```text

AI-ArtBench combines generated artworks with ArtBench-10 human images \cite{p1,artbench}. All 185,015 release files decode as RGB JPEG (Table~\ref{tab:t2}); no EXIF or embedded ICC profiles are supplied. Human and LD images are native $256^2$; SD is native $768^2$ and remains a separate resized descriptive sensitivity. Table~\ref{tab:t3} gives grouped development, validation and test counts. Five exact duplicate pairs and conservative perceptual/source links are joined before splitting; the perceptual rule requires both 64-bit pHash and dHash distances at most four, using ImageHash \cite{imagehash}. Transitive source links remain split-disjoint.

```

After:

```text

AI-ArtBench joins generated images with ArtBench-10 human art \cite{p1,artbench}. All 185,015 files are RGB JPEG without EXIF/ICC (Table~\ref{tab:t2}); Human/LD are native $256^2$, while SD is native $768^2$ and resized only descriptively. Before freezing splits (Table~\ref{tab:t3}), transitive grouping joins five exact duplicate pairs, conservative source links and paired 64-bit pHash/dHash distances at most four, using ImageHash \cite{imagehash}.


```


## Final space offset 5: IV-B metric definitions avoid repeating abstract/companion caption

Offset additions with duplicated prose; no type/margin reduction or empirical-result change.

Before:

```text
AUROC evaluates ranking; precision, recall and F1 use AI-positive labels. Accuracy equals balanced accuracy on the balanced primary test. Fifteen-bin expected calibration error (ECE) measures probability calibration. Macro-style AUROC/F1 average the ten styles. Label-based origin silhouette \cite{silhouette} is $(b-a)/\max(a,b)$, with within-origin mean distance $a$ and other-origin distance $b$. Unsupervised $k=2$ ARI compares clusters with origin only after fitting. Neighborhood trustworthiness $T(15)$ \cite{venna} penalizes false neighbors and continuity $C(15)$ penalizes lost neighbors on a fixed 3,000-artwork subset. The latter is unrelated to complexity or regularization despite the conventional shared letter.
```

After:

```text
Fifteen-bin expected calibration error (ECE) measures calibration. Origin silhouette \cite{silhouette} is $(b-a)/\max(a,b)$ for mean same-origin distance $a$ and other-origin distance $b$; unlabeled $k=2$ ARI compares clusters with origin after fitting. On a fixed 3,000-artwork subset, trustworthiness $T(15)$ \cite{venna} penalizes false neighbors and continuity $C(15)$ lost neighbors. This continuity is distinct from complexity and regularization; threshold/macro metrics are defined in Table~\ref{tab:essential}.
```


## Final space offset 6: VIII-C concise external-validity scope

Offset additions with duplicated prose; no type/margin reduction or empirical-result change.

Before:

```text
\textit{External validity:} only ten release movements and two primary origins are evaluated. Separate artist/style/generator holdouts, raw museum captures and new generator versions remain untested. SD resizing and mixed-source composition limit transportability.
```

After:

```text
\textit{External validity:} ten release movements and two primary origins are tested; SD resizing and mixed-source composition restrict transfer, with no separate artist/style/generator holdouts.
```


## Final space offset 7: Appendix A

Keep unique settings, hash, hardware limitations and scoped runtimes; remove duplicated version/caveat wording.

Before:

```text
The frozen cohort SHA256 is \texttt{e27a00766ad8825201aac6d4167a5a98b}\allowbreak\texttt{319d5b18b136ffb20d5765073472936}. Split IDs and resamples accompany \href{https://github.com/wasil-7/explainable-diffusion-art-analytics}{the official repository}. Seeds: analysis 42; t-SNE 42--46; supplementary repartitions 43--47.

L-BFGS uses unweighted L2, max\_iter 2000 and tol $10^{-4}$. PCA uses three components/full SVD; t-SNE uses random initialization, automatic learning rate, 1,000 iterations and perplexity 15/30/50. NumPy Lloyd clustering uses k=2, k-means++ initialization, 20 starts and at most 300 iterations. Encoder extraction averages four 224-pixel quadrant views with ImageNet normalization, CUDA FP16, 32-quadrant batches and four workers.

Recorded environment: Windows 11 (26300), CUDA 12.4, driver 621.14; original cuDNN version unrecorded and revision import unavailable. Section IV and the pinned release specify package versions.

Recorded probe fitting/tuning seconds (handcrafted, FFT, metadata, ResNet-50, DINOv2): 7.00, 0.47, 0.11, 12.49, 1.70. Encoder cache-state seconds: 2916.85 and 5020.19 for ResNet-50 and DINOv2, excluding cold imports and interrupted earlier work. Released runtime records distinguish cache-reusing resumes; no end-to-end total is reconstructed. 

```

After:

```text
The frozen cohort SHA256 is \texttt{e27a00766ad8825201aac6d4167a5a98b}\allowbreak\texttt{319d5b18b136ffb20d5765073472936}; IDs/resamples accompany \href{https://github.com/wasil-7/explainable-diffusion-art-analytics}{the official repository}. Seeds: original 42, t-SNE 42--46, repartitions 43--47.

Unweighted L2 L-BFGS: max\_iter 2000, tol $10^{-4}$. PCA: three components/full SVD. t-SNE: random initialization, automatic learning rate, 1,000 iterations, perplexity 15/30/50. NumPy Lloyd: k=2, k-means++, 20 starts, max 300 iterations. Encoders average four normalized 224-pixel views; CUDA FP16, 32-quadrant batches, four workers.

CUDA 12.4, driver 621.14; original cuDNN unrecorded and revision import unavailable. Probe fitting/tuning seconds (handcrafted, FFT, metadata, ResNet-50, DINOv2): 7.00, 0.47, 0.11, 12.49, 1.70. Encoder cache-state seconds: 2916.85/5020.19, excluding cold imports/interrupted work. Resume timings are not end-to-end totals; full records accompany the release.

```


## Final Table IV layout

The requested accuracy/precision/recall and original macro scores are folded into Table IV instead of adding a second table float. No metrics are dropped. Selected solver C/thresholds move to Appendix A. Fonts and margins are unchanged.

Before:
```latex
\begin{table*}[t]
\caption{Frozen primary-test ranking, F1 and calibration (6,000 artworks). Percentile 95\% intervals resample source groups within origin 1,000 times and retain the fitted models/thresholds. C is the selected solver regularization value.}\label{tab:t4}
\centering\footnotesize\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.10}
\begin{tabularx}{\textwidth}{>{\hsize=1.263\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=1.940\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=1.489\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=0.451\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=0.361\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=0.496\hsize\linewidth=\hsize\raggedright\arraybackslash}X}
\toprule
\textbf{Probe} & \textbf{AUROC [95\% CI]} & \textbf{F1 [95\% CI]} & \textbf{ECE} & \textbf{C} & \textbf{Threshold}\\\midrule
{}Handcrafted (104-D) & 0.982415 [0.978332, 0.986003] & 0.9420 [0.9347, 0.9487] & 0.0154 & 10.0000 & 0.4380\\
{}FFT-only (36-D) & 0.683901 [0.664844, 0.701442] & 0.6830 [0.6605, 0.7027] & 0.0500 & 10.0000 & 0.4036\\
{}Metadata-only & 1.000000 [1.000000, 1.000000] & 0.9997 [0.9992, 1.0000] & 0.1940 & 0.0010 & 0.6415\\
{}ResNet-50 (frozen) & 0.999945 [0.999868, 0.999988] & 0.9972 [0.9957, 0.9985] & 0.0022 & 1.0000 & 0.7827\\
{}DINOv2 (frozen) & 0.999688 [0.999296, 0.999939] & 0.9955 [0.9936, 0.9973] & 0.0021 & 1.0000 & 0.2774\\
\bottomrule\end{tabularx}
\end{table*}

```

After:
```latex
\begin{table*}[t]
\caption{Primary-test metrics (6,000 artworks). Accuracy equals balanced accuracy (BA); precision/recall/F1 use diffusion-positive labels. Macro scores average ten styles. Percentile 95\% intervals use 1,000 origin-stratified source-group draws with fits/thresholds fixed. Selected settings appear in Appendix A.}\label{tab:t4}\label{tab:essential}
\centering\footnotesize\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.10}
\begin{tabularx}{\textwidth}{>{\hsize=1.471\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=2.059\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=1.353\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=0.553\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=0.553\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=0.553\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=0.494\hsize\linewidth=\hsize\raggedright\arraybackslash}X>{\hsize=0.965\hsize\linewidth=\hsize\raggedright\arraybackslash}X}
\toprule
\textbf{Probe} & \textbf{AUROC [95\% CI]} & \textbf{F1 [95\% CI]} & \textbf{Acc./BA} & \textbf{Prec.} & \textbf{Recall} & \textbf{ECE} & \textbf{Macro AUC/F1}\\\midrule
{}Handcrafted (104-D) & 0.982415 [0.978332, 0.986003] & 0.9420 [0.9347, 0.9487] & 0.9407 & 0.9213 & 0.9637 & 0.0154 & 0.9817/0.9422\\
{}FFT-only (36-D) & 0.683901 [0.664844, 0.701442] & 0.6830 [0.6605, 0.7027] & 0.5960 & 0.5620 & 0.8703 & 0.0500 & 0.6909/0.6826\\
{}Metadata-only & 1.000000 [1.000000, 1.000000] & 0.9997 [0.9992, 1.0000] & 0.9997 & 1.0000 & 0.9993 & 0.1940 & 1.0000/0.9997\\
{}ResNet-50 (frozen) & 0.999945 [0.999868, 0.999988] & 0.9972 [0.9957, 0.9985] & 0.9972 & 0.9973 & 0.9970 & 0.0022 & 0.9999/0.9972\\
{}DINOv2 (frozen) & 0.999688 [0.999296, 0.999939] & 0.9955 [0.9936, 0.9973] & 0.9955 & 0.9947 & 0.9963 & 0.0021 & 0.9997/0.9955\\
\bottomrule\end{tabularx}
\end{table*}

```


## Appendix de-duplication

Remove seed/encoder settings already explicit in the main text and algorithm; shorten runtime labels without changing values or timing scope.

Before:
```latex
The frozen cohort SHA256 is \texttt{e27a00766ad8825201aac6d4167a5a98b}\allowbreak\texttt{319d5b18b136ffb20d5765073472936}; IDs/resamples accompany \href{https://github.com/wasil-7/explainable-diffusion-art-analytics}{the official repository}. Seeds: original 42, t-SNE 42--46, repartitions 43--47.

Unweighted L2 L-BFGS: max\_iter 2000, tol $10^{-4}$. PCA: three components/full SVD. t-SNE: random initialization, automatic learning rate, 1,000 iterations, perplexity 15/30/50. NumPy Lloyd: k=2, k-means++, 20 starts, max 300 iterations. Encoders average four normalized 224-pixel views; CUDA FP16, 32-quadrant batches, four workers.

CUDA 12.4, driver 621.14; original cuDNN unrecorded and revision import unavailable. Probe fitting/tuning seconds (handcrafted, FFT, metadata, ResNet-50, DINOv2): 7.00, 0.47, 0.11, 12.49, 1.70. Encoder cache-state seconds: 2916.85/5020.19, excluding cold imports/interrupted work. Resume timings are not end-to-end totals; full records accompany the release.

Selected $C$: 10 (handcrafted/FFT), 0.001 (metadata), 1 (both encoders). Thresholds in Table~\ref{tab:t4} order: 0.4380, 0.4036, 0.6415, 0.7827, 0.2774.

```

After:
```latex
The frozen cohort SHA256 is \texttt{e27a00766ad8825201aac6d4167a5a98b}\allowbreak\texttt{319d5b18b136ffb20d5765073472936}; IDs/resamples accompany \href{https://github.com/wasil-7/explainable-diffusion-art-analytics}{the official repository}. 

Unweighted L2 L-BFGS: max\_iter 2000, tol $10^{-4}$. PCA: three components/full SVD. t-SNE: random initialization, automatic learning rate, 1,000 iterations, perplexity 15/30/50. NumPy Lloyd: k=2, k-means++, 20 starts, max 300 iterations. 

CUDA 12.4, driver 621.14; original cuDNN unrecorded and revision import unavailable. Fit/tune seconds (Table~\ref{tab:t4} order): 7.00, 0.47, 0.11, 12.49, 1.70. ResNet-50/DINOv2 cache-state times 2916.85/5020.19 s exclude cold imports/earlier interruptions; resume timings are not end-to-end totals.

Selected $C$: 10 (handcrafted/FFT), 0.001 (metadata), 1 (both encoders). Thresholds in Table~\ref{tab:t4} order: 0.4380, 0.4036, 0.6415, 0.7827, 0.2774.

```


## Final repeated-prose cut

Preserve assumptions and definitions; unit-test details remain in release records.

Before: Subject and encoding exchangeability is unsupported, so adjusted probabilities and raw passes remain exploratory regardless of numerical threshold satisfaction.

After: With subject/encoding exchangeability unverified, adjusted probabilities remain exploratory.


## Final repeated-prose cut

Preserve assumptions and definitions; unit-test details remain in release records.

Before: conditional on frozen fits means that fitted preprocessing, model parameters and thresholds are held fixed during resampling.

After: conditional on frozen fits means preprocessing, coefficients and thresholds stay fixed.


## Final repeated-prose cut

Preserve assumptions and definitions; unit-test details remain in release records.

Before: Seven synthetic feature tests and three numerical tests check bounds, tiling, spectra, distances, randomization and clustering; they do not establish attribution validity.

After: Synthetic tests cover feature invariants and numerical routines, not attribution validity.

## Robustness interval alignment
Before: absolute AUROC intervals from a separate valid summary. After: paired AUROC differences and their exact Table XII intervals, original a zero reference by definition. Reason: chart and table now report the identical estimand; no inference rerun.

## Fresh review integration
Independent review: qa/FRESH_INDEPENDENT_REVIEW.md. Expanded HSV, SD and ARI at first use; named the handcrafted abstract probe. Defined bilinear down/up perturbation and the exact silhouette-ratio/rank-rho targets. Appendix now describes prepared local availability, not already-published artifacts. Exact prior wording is preserved in qa/complete_text_changes.diff; no results changed. Reproduction command/output mapping added to release documentation. Separate audit attachment remains unprovided.

## Final source, figures and package polish
Reasoned semantic edits above are supplemented by the complete before/after text diff in qa/complete_text_changes.diff. All eleven static composites were redrawn from saved CSVs and actual gallery assets; the dashboard was recaptured, never synthesized. Small probabilities use fixed precision or a valid lower-than bound. Word small tables now keep rows together. Added supplementary.pdf, 12-step source-backed changes/crosswalk, audit-claim dispositions, explicit source metadata receipt, exact reproduction command map, current compliance/verification/review/summary documents and portable table templates. No empirical pipeline rerun, font/margin shrink or headline change. Previously delivered versions are archived before final copies replace them.

## Reproduction review follow-ups
Before: per-style intervals attributed too broadly to supplementary-statistics script; point CSV export omitted; stale state/excluded-cache combination not prevented by instructions. After: per-style intervals attributed to ablations.py, publication_figures.py exports refreshed PCA/H-C/tSNE CSVs before final layout generation, and explicit isolated-workcopy state preparation archives existing derived folders with validated paths and no deletion. Reason: exact executable command mapping and safe cache provenance. Synthetic fixture test passed; no actual experiments executed. Fresh reviewer recheck reports no blocker within scope; missing separate audit remains open.

## 22 November2026 — final forensic audit corrections
- Fig.3C p5: crossing annotation leaders replaced by aligned silhouette/ARI row strips; first attempt had crowded labels, corrected with alternating row keys and short endpoint ticks. All10style rows retained; caption explicitly maps rows to B1. No numeric values changed.
- VII-B p9: explicitly states no equal-encoding retraining was run; stress tests retain original fit.
- Availability p11: public original release acknowledged; audited update explicitly requires next commit.
- Git byte-integrity: added .gitattributes '* -text' after confirming remote CSVs were LF-normalized versions of local CRLF files. Exact byte manifests require the updated push.
- GCR ZIP changed from flattened legacy layout to canonical root paper.pdf/paper.docx/supplementary.pdf/latex_source.zip plus release/. Source/Word rebuilt and all copies synchronized.
- Supplied final audit request resolved earlier missing-audit input; FINAL_AUDIT.md and independent-review evidence added. Earlier empty-remote/missing-input statements are historical, superseded by this report.
