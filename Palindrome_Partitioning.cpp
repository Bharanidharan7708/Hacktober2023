// Leetcode : 131. Palindrome Partitioning (https://leetcode.com/problems/palindrome-partitioning/)

class Solution {
public:
	vector<vector<string>> partition(string s) {
		vector<vector<string>> ans;
		vector<string>path;
		int n = s.size();
		solve(0, n, s, path, ans);
		return ans;
	}

	void solve(int index, int n, string s, vector<string>&path, vector<vector<string>>&ans)
	{
		if (index == n)
		{
			ans.push_back(path);
			return;
		}
		for (int i = index; i < n; i++)
		{
			if (s[i] == s[index] && ispalindrome(index, i, s))
			{
				path.push_back(s.substr(index, i - index + 1));
				solve(i + 1, n, s, path, ans);
				path.pop_back();
			}
		}
	}

	bool ispalindrome(int start, int end, string &s)
	{
		while (start < end)
		{
			if (s[start++] != s[end--])
			{
				return false;
			}
		}
		return true;
	}
};
