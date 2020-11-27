# spell_checker_korean
hanspell 코드를 참고하여 쓰기 편하게 만들어 보았습니다.

## 실행 방법
실행 방법은 아래와 같습니다.
```
  python run_spellcheck.py --input_dir <input_directory> --output_dir <output_directory> --output_flag corrected_ --num_cores 16 --delimeter \n
```
- input_dir: 입력 파일들이 위치한 폴더의 경로입니다.
- output_dir: 출력 파일들이 위치한 폴더의 경로입니다.
- output_flag: 출력 파일의 앞에 붙는 문자열입니다(기본: 'corrected_').
- num_cores: 프로세싱에 사용할 cpu의 코어 개수입니다(기본: 사용 가능한 모든 cpu core).
- delimiter: 입력 파일을 문장 또는 문단 별로 나누기 위한,구분자입니다(기본: '\n'; delimiter는 hanspell에서 사용하고 있는 네이버 맞춤법 교정기의 제한된 글자 수(500자) 만큼 문장 또는 문단을 나누고 결합하기 위해 필요합니다.).


## 주의 사항
- 해당 코드는 cpu 멀티 프로세싱을 통해 한글 교정을 진행합니다.
- 본 코드는 py-hanspell(https://github.com/ssut/py-hanspell) 코드를 바탕으로 수정하여 제작된 코드 입니다.
