def vowel_remover(text):
    """Remove vowels from a string while preserving consonants, spaces, and punctuation.

    Contract & Boundaries:
        Preconditions:
            - Source line 24: `for l in text:` establishes that `text` must be iterable.
            - Source line 25: `l.lower() not in "aeiou"` establishes that each element `l`
              must provide a `.lower()` method.
            - Source line 26: `string += l` establishes that `l` can be concatenated to a `str`.
        Supported Domain:
            - Valid Interior: Strings containing a mixture of vowels, consonants, numbers,
              and symbols (e.g. "hello world!").
            - Valid Boundaries:
                * Smallest valid input: empty string `""` -> `""`.
                * All vowels: `"aeiouAEIOU"` -> `""`.
                * No vowels: `"rhythm"` -> `"rhythm"`.
                * Single character consonant: `"x"` -> `"x"`.
                * Single character vowel: `"e"` -> `""`.
                * Whitespace and symbols only: `" 123 !@# "` -> `" 123 !@# "`.
            - Explicitly Unsupported Values:
                * Non-iterables (e.g. `None`, `42`) raise `TypeError` at line 24.
                * Iterables containing elements without `.lower()` raise `AttributeError` at line 25.
        Returns:
            str: Accumulator string with all vowels removed.
        Mutation:
            None. Pure function.
    """
    string = ""
    for l in text:
        if l.lower() not in "aeiou":
            string += l
    return string

# this code runes on only this file
if __name__=="__main__":
    print(vowel_remover("hello world!"))
