## ファイルの説明
+ __sudoku_solver.py__  
sat13を用いて数独のパズルを解くpythonプログラム。  
実行時に数独のテキストファイルを引数に指定する。  
```python sudoku_solver.py sudoku_ex.txt```

+ **sudoku_hoge.txt**  
数独の問題を記したテキストファイル。  
sudoku_hard.txtは最も困難な数独パズルと言われている問題([参考資料](https://www.sentohsharyoga.com/ja/puzzle/blog/entry/sudoku_most_difficult))。  
sudoku_unable.txtはパズルの解が存在しない例の問題。

+ **sudoku_hoge.sat**  
pythonプログラムを実行することで生成されるsatファイル。
