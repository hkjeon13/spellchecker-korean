# spell_checker_korean
hanspell 코드를 참고하여 쓰기 편하게 만들어 보았습니다.

## 실행 방법
실행 방법은 아래와 같습니다.
```
  python run_spellcheck.py --input_dir <input_directory> --output_dir <output_dir> --output_flag corrected_ --num_cores 16 --delimeter \n
```

## 주의 사항
- 해당 코드는 멀티 프로세싱을 통해 한글 교정을 진행합니다.
- 본 코드는 py-hanspell(https://github.com/ssut/py-hanspell) 코드를 바탕으로 수정하여 제작된 코드 입니다.
