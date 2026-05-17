# internal support for versioning.
# not to be used externally; just to make upgrading versions easier.


# So why do this? Because I suck at adding new versions and this would
# make things much more convenient and easier.

class _V:
    def __new__(cls, val):
        self = super().__new__(cls)
        try:
            major, minor = map(int, val.lstrip("v").split("."))
        except ValueError:
            raise ValueError(f"Invalid version format: {val}, expected 'major.minor'")
        self._major, self._minor = map(abs, [major, minor]) # negative? positify it
        return self
    
    def __gt__(self, other):
        if isinstance(other, _V):
            return (self._major, self._minor) > (other._major, other._minor)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, _V):
            return (self._major, self._minor) < (other._major, other._minor)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, _V):
            return (self._major, self._minor) == (other._major, other._minor)
        return NotImplemented

    def __ge__(self, other):
        return not (self < other)

    def __le__(self, other):
        return not (self > other)
    
    def __repr__(self):
        return f"v{self._major}.{self._minor}"
    
    __str__ = __repr__ # bad idea but wth

    def __hash__(self):
        return hash((self._major, self._minor))
