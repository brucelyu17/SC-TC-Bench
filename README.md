# Characterizing Bias: Benchmarking Large Language Models in Simplified versus Traditional Chinese

[Hanjia Lyu](https://brucelyu17.github.io/)<sup>1</sup>, [Jiebo Luo](https://www.cs.rochester.edu/u/jluo/)<sup>1</sup>, [Jian Kang](https://jiank2.github.io/)<sup>1</sup>, [Allison Koenecke](https://koenecke.infosci.cornell.edu/)<sup>2</sup>

<sup>1</sup> University of Rochester

<sup>2</sup> Cornell University

Accepted for publication in [FAccT 2025](https://facctconference.org/2025/)

Will also be presented at [IC2S2 2025](https://www.ic2s2-2025.org/)

## Example Usage

* Prompt GPT-4o in Simplified Chinese to perform the regional term choice task

```bash
python infer.py --llm gpt4o --task term --lang simplified --prompt_id 1
```

* Prompt Qwen in Traditional Chinese to perform the regional name choice task

```bash
python infer.py --llm qwen --task name --lang traditional --prompt_id 1
```

## Datasets

### Regional Term

* `prompt/regional_term/{language}_{prompt_id}.csv`

These datasets contain the prompts of the regional term choice task. `prompt_id` represents the prompt version.

### Regional Name

* `prompt/regional_name/{language}_{prompt_id}.csv`

These datasets contain the prompts of the regional name choice task. `prompt_id` represents the research questions in Section 4. `prompt_id_1`: Section 4.1, `prompt_id_2`: Section 4.3.1, `prompt_id_3`: Section 4.4.



## Citation
```
@inproceedings{sctcbench-facct25,
title={Characterizing Bias: Benchmarking Large Language Models in Simplified versus Traditional Chinese},
author={Lyu, Hanjia and Luo, Jiebo and Kang, Jian and Koenecke, Allison},
year={2025},
isbn = {9798400714825},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3715275.3732182},
doi = {10.1145/3715275.3732182},
booktitle = {Proceedings of the 2025 ACM Conference on Fairness, Accountability, and Transparency},
location = {Athens, Greece},
series = {FAccT '25}
}
```