from typing import Optional


class Scope(dict):
    def __init__(self, parent: Optional['Scope'] = None):
        super().__init__()
        self.parent: Scope | None = parent

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            if self.parent:
                try:
                    return self.parent[item]
                except KeyError:
                    pass
            raise NameError(f'Unknown variable {item}')
