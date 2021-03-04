"""
https://leetcode.com/problems/delete-operation-for-two-strings/

Given two words word1 and word2, find the minimum number of steps required to make word1 and word2 the same,
where in each step you can delete one character in either string.

Example 1:
Input: "sea", "eat"
Output: 2
Explanation: You need one step to make "sea" to "ea" and another step to make "eat" to "ea".

Note:
The length of given words won't exceed 500.
Characters in given words can only be lower-case letters.
"""
from functools import lru_cache
from typing import Callable

from util import stopwatch


class SolutionRecur:
    """
    Complexity Analysis

Time complexity : O(m*n). memo (lru_cache) array of size mxn needs to be filled once. Here, mm and nn refer to the length of the strings word1 and word2 respectively.

Space complexity : O(m*n). memo (lru_cache) array of size mxn. Also, The depth of the recursion tree will go up to max(m,n).
    """

    def minDistance(self, word1: str, word2: str) -> int:
        import sys
        sys.setrecursionlimit(5000)

        @lru_cache(maxsize=None)
        def minDel(p1, p2):
            if p1 == len(word1) or p2 == len(word2):
                return abs(len(word1) + len(word2) - p1 - p2)

            if word1[p1] == word2[p2]:
                return minDel(p1 + 1, p2 + 1)
            else:
                return 1 + min(minDel(p1 + 1, p2), minDel(p1, p2 + 1))

        return minDel(0, 0)


class SolutionDpLcs:
    """
Time complexity : O(m*n). We need to fill in the dp array of size mXn. Here, m and n refer to the lengths of word1 and word2.

Space complexity : O(m*n). dp array of size mXn is used.

    """

    def minDistance(self, word1: str, word2: str) -> int:
        # java equivalent
        # int[][] dp = new int[s1.length() + 1][s2.length() + 1];
        dp = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]
        for i in range(len(word1) + 1):
            for j in range(len(word2) + 1):
                if i == 0 or j == 0:
                    continue
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        lcs = dp[len(word1)][len(word2)]
        return len(word1) + len(word2) - 2 * lcs


class SolutionDpNoLcs:
    """
Time complexity : O(m*n). We need to fill in the dp array of size mXn. Here, m and n refer to the lengths of word1 and word2.

Space complexity : O(m*n). dp array of size mXn is used.

    """

    def minDistance(self, word1: str, word2: str) -> int:
        # java equivalent
        # int[][] dp = new int[s1.length() + 1][s2.length() + 1];
        dp = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]
        for i in range(len(word1) + 1):
            for j in range(len(word2) + 1):
                if i == 0 or j == 0:
                    dp[i][j] = i + j
                elif word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])

        return dp[len(word1)][len(word2)]


class SolutionDp1D:
    """
Complexity Analysis

Time complexity : O(m*n). We need to fill in the dp array of size n, m times. Here, m and n refer to the lengths of s1 and s2.

Space complexity : O(n). dp array of size n is used.

    """

    def minDistance(self, s1: str, s2: str) -> int:

        dp = [i for i in range(len(s2) + 1)]

        for i in range(len(s1) + 1):
            temp = [0] * (len(s2) + 1)
            for j in range(len(s2) + 1):
                if i == 0 or j == 0:
                    temp[j] = i + j
                elif s1[i - 1] == s2[j - 1]:
                    temp[j] = dp[j - 1]
                else:
                    temp[j] = 1 + min(dp[j], temp[j - 1])
            dp = temp

        return dp[len(s2)]


class Solution:
    """
    1-D Dynamic Programming

Time complexity : O(m*n). We need to fill in the dp array n*m times. Here, m and n refer to the lengths of word1 and word2.

Space complexity : O(min(m, n)). dp array of size min(m,n) is used.

    """

    def minDistance(self, word1: str, word2: str) -> int:
        # last bit of optimization - use an array of minimal size
        if len(word1) > len(word2):
            word1, word2 = word2, word1
        # basically we compare substrings of word1 with empty space, i.e. how many chars we need to remove until 2 whitespaces will be equal
        dp = [i for i in range(len(word1) + 1)]

        for j in range(1, len(word2) + 1):
            # store intermediate last value from the previous run and prepare for the current one
            last, dp[0] = dp[0], j
            for i in range(1, len(word1) + 1):
                current = dp[i]
                dp[i] = last if word1[i - 1] == word2[j - 1] else 1 + min(dp[i], dp[i - 1])
                last = current

        return dp[len(word1)]


@stopwatch
def test(solution: Callable):
    assert solution("sea", "eat") == 2
    assert solution("sea", "sea") == 0
    assert solution("timea", "time") == 1
    assert solution("a", "b") == 2
    assert solution("", "b") == 1
    assert solution("dinitrophenylhydrazine", "acetylphenylhydrazine") == 11
    assert solution(
        "hlhtwylgbnhnadlyzcfxovbycjwuvlctenacwmronjfuupwjmsuqcrwytppgvdupyoiybzvtcmeueztbehidonocsjimuikuftsflpprvgcmqmvsfhkjmrxpqmsyxlkuorfimhibjcycuaxihqkdgvkycacwujrjenovghotpobusxdiurbrybrancdrxgiczieesobx",
        "ffdkrdukqemsyjeukhixjhwmvsdtnsbcrlmzxwxugqnnaufbrhgwbmfenjkxpkonnlrqfovfpuhgixavntyiquqcdtqxcpkigrvdjwbezsniizqvelueliepawxanmicuslwsnilpdmoheaicbdlyssmupeklytnppxhzdvrclmrofsvhnqjuegmcnsgheldxhirvlbpopotvjvnhaxprlwuxozewksltnrarufanhzxpjshuiodhizpnedewcqdzpedskysdzrnpcpacwfpusoeqcooyxjaiwxsawkfxkrj") \
           == 340
    assert solution(
        "golslpxkqfgqhfvxhchoupeifgwpjqzrvzmdyxdlzufjpmmgvcxwhomynhvppimqwqmhcqxflefkcdafoijvwrijdtnnxhwxsmloyrvjwdjprxpfazzuvmnylaastotshilfmllrsqwejcfoykzwuftdhxdynkxivvbkboxoadxkkpwkqxruweqcurivdcnyblbtsklmamuxfkzrgapfjodpwmwllkqyyfsgvrtaehbxxnddlruecidrbcyukbtaivpdowlfoebvqrdghdyijispqjnisxtekceaupbhfadnuvgxknakcqjkntdzepzivpjbqggrsjhslftxzkrktgyzesniequbdglnhpcfdnyakwidyfslwgoancwsibqtkapzomzuaoazplvi",
        "dlhtdovkgocsfayhjnfycpwlaoxarsshllwsmgzfduuqrepxxkgomycrudsexvbwvrhdpbofejzivkydfpkebzlyvzgakxaiscazydyhfjvssvvxkxexauzvgtznuhcqyzxggwtagynudgkrjatlmjuzolgliktvgjjrbyycbcrjcxfciaxtpfmmhcwfkhilmkontwwbzbtgdcdblxhaedlxftaevcltjfsmpmyxrmqptogsqifoesjcrdwnhaxngqdvamrqhvfibtsizvhtjkgtbqjbndebfjhmcovmpcwxbakithmsmlmlybodunmgfnildprombrgitflxeunlaqufxmhstrbkabpmmeyiavdxtwqaouqtrcoasxerbfkhgfuchzbmrasfbzugpfkimdbvvcfkvhrletzycvwqmayuklepycszrhvmgdmhywhcvpiayycokdtzazsrzttpeffoxaddzqlnnybqixxnssxdqeusmty") \
           == 622
    assert solution(
        "long_xkqfgqhfvxhchoupeifgwpjqzrvzmdyxdlzufjpmmgvcxwhomynhvppimqwqmhcqxflefkcdafoijvwrijdtnnxhwxsmloyrvjwdjprxpfazzuvmnylaastotshilfmllrsqwejcfoykzwuftdhxdynkxivvbkboxoadxkkpwkqxruweqcurivdcnyblbtsklmamuxfkzrgapfjodpwmwllkqyyfsgvrtaehbxxnddlruecidrbcyukbtaivpdowlfoebvqrdghdyijispqjnisxtekceaupbhfadnuvgxknakcqjkntdzepzivpjbqggrsjhslftxzkrktgyzesniequbdglnhpcfdnyakwidyfslwgoancwsibqtkapzomzuaoazplvi",
        "short_yhjnfycpwlaoxarsshllwsmgzfduuq") \
           == solution(
        "short_yhjnfycpwlaoxarsshllwsmgzfduuq",
        "long_xkqfgqhfvxhchoupeifgwpjqzrvzmdyxdlzufjpmmgvcxwhomynhvppimqwqmhcqxflefkcdafoijvwrijdtnnxhwxsmloyrvjwdjprxpfazzuvmnylaastotshilfmllrsqwejcfoykzwuftdhxdynkxivvbkboxoadxkkpwkqxruweqcurivdcnyblbtsklmamuxfkzrgapfjodpwmwllkqyyfsgvrtaehbxxnddlruecidrbcyukbtaivpdowlfoebvqrdghdyijispqjnisxtekceaupbhfadnuvgxknakcqjkntdzepzivpjbqggrsjhslftxzkrktgyzesniequbdglnhpcfdnyakwidyfslwgoancwsibqtkapzomzuaoazplvi",
    )


if __name__ == '__main__':
    test(SolutionRecur().minDistance)
    test(SolutionDpLcs().minDistance)
    test(SolutionDpNoLcs().minDistance)
    test(SolutionDp1D().minDistance)
    test(Solution().minDistance)
