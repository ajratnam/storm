## Latest Commit
- Added more **methods** to **Paginator**.
- Added dummy **parse** method to **Tokenizer**.
- Created **CHANGELOG.md**.
- Changed the **error* raised by **enforcer**
- Moved **Token** type to **tokens.py**.
- Updated most of the **functions** to use **enforce_type**.

## 19.01.2022 ([4484b537](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4))
- Added **body typehint** to [Executor](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-73fd8e83d3fa7549ec08fa8bacacf78afba2128315b647cbd15b0ea932278f84R7), [TokenType](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-1af35f03aeaa196fe030d54230728c3f21cdcce78bdda70764e919b4a2a4c6bfR3) and [Token](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-d138c856daaf4a8615fb0a495b41c6168479dc7613918686a64276897683b7c9R6).
- Added **return type** to [execute](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-73fd8e83d3fa7549ec08fa8bacacf78afba2128315b647cbd15b0ea932278f84R9).
- Created [Paginator](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-f033f0ad91830d3786b9510773119589ee24cd96053073f1eb5ad2d6c09dd811R72-R85) for **future usage**.
- Created [check_instance](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-f033f0ad91830d3786b9510773119589ee24cd96053073f1eb5ad2d6c09dd811R43-R69) for **instance checking of generics**.
- Created [get_type](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-f033f0ad91830d3786b9510773119589ee24cd96053073f1eb5ad2d6c09dd811R29-R34) and [get_type_repr](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-f033f0ad91830d3786b9510773119589ee24cd96053073f1eb5ad2d6c09dd811R37-R40) to find the **type** and **repr of the type** of the object.
- Updated [Executor](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-f033f0ad91830d3786b9510773119589ee24cd96053073f1eb5ad2d6c09dd811R19) to use the **new** check_instance.
- Updated [Executor](https://github.com/ajratnam/storm/commit/4484b53700ff09897c0bdd568d0df1efdcdd57d4#diff-f033f0ad91830d3786b9510773119589ee24cd96053073f1eb5ad2d6c09dd811R20) to raise **better error**.

## 12.01.2022 ([c475409e](https://github.com/ajratnam/storm/commit/c475409edff82077f9fbe55232edc8a7ec9ce76e))
- Created **decorator** [enforce_type](https://github.com/ajratnam/storm/commit/c475409edff82077f9fbe55232edc8a7ec9ce76e#diff-f033f0ad91830d3786b9510773119589ee24cd96053073f1eb5ad2d6c09dd811R9-R23) to **force typehints**.
- Created **dummy class** for [Executor](https://github.com/ajratnam/storm/commit/c475409edff82077f9fbe55232edc8a7ec9ce76e#diff-73fd8e83d3fa7549ec08fa8bacacf78afba2128315b647cbd15b0ea932278f84R4-R12) which **executes** the tokenized code.
- Created **new types** [Token](https://github.com/ajratnam/storm/commit/c475409edff82077f9fbe55232edc8a7ec9ce76e#diff-d138c856daaf4a8615fb0a495b41c6168479dc7613918686a64276897683b7c9R4-R10) and [TokenType](https://github.com/ajratnam/storm/commit/c475409edff82077f9fbe55232edc8a7ec9ce76e#diff-1af35f03aeaa196fe030d54230728c3f21cdcce78bdda70764e919b4a2a4c6bfR1-R3).