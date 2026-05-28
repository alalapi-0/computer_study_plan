# Round 02 命令小抄（可手动补充）

## 重定向与管道

```bash
echo "text" > file.txt
echo "text" >> file.txt
grep "error" app.log | wc -l
sort labels.txt | uniq
```

## 脚本执行

```bash
bash count_errors.sh
bash show_args.sh one two
```

## Git 最小闭环

```bash
git init
git status
git add README.md
git commit -m "init repository"
git log --oneline
```

## 自检问题

- [ ] 我能解释 `>` 与 `>>` 的差异。
- [ ] 我能用一条管道统计错误日志条数。
- [ ] 我能独立做出至少 2 次 Git 提交。
