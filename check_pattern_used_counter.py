from tabnanny import check
import pandas as pd
import csv
from functools import reduce
import random

'''
특정 태그 데이터가 문장 내에서 등장하는 패턴을 찾기 위한 코드
찾고 & O 태깅 / 찾고 & 정보 채워넣기 & 태깅 
counter 활용하여 대체 & 채우기 동시에 
'''

def str_random(start, end):
        return str(random.randint(start, end))
    
def make_random_number(start, random_size):
        result = start
        for i in range(random_size):
            result += str_random(0, 4)
        return result
    
# def fill_deid(input):
    
#     aaa = aaa.strip()
#     aaa = ' '.join(aaa.split()) # 다중 공백 제거
#     tokens = aaa.split(' ')
    

def writedata(aaa, f, opt):
    
    '''
    ㅇㅇㅇㅇ ㅇㅇㅇㅇ ㅇㅇㅇㅇ ㅇㅇㅇㅇ 태깅 ID_CARD_B ID_CARD_I ID_CARD_I ID_CARD_I로 처리하기
    ㅇㅇㅇㅇ 시작 인덱스 반환 -> 거기서부터 i~i+3까지 
    카드 회사는 어떻게 하지?
    농협 우리 신한 삼성 비씨 국민 롯데 를 포함하고 있으면 B_SS_BRAND로 일단 처리
    +++ 태깅과 동시에 데이터 채워넣기
    '''
    aaa = aaa.strip()
    aaa = ' '.join(aaa.split()) # 다중 공백 제거
    tokens = aaa.split(' ')
    # print(tokens)

    tags = ''
    card_brands = ["농협", "우리", "신한", "삼성", "비씨", "국민", "롯데", "카카오", "하나", "현대", 
                   "농협카드", "우리카드", "신한카드", "삼성카드", "비씨카드", "국민카드", "롯데카드", "카카오카드", "하나카드", "현대카드"]
    
    

    num_idx = 0 # 이렇게 하게 되면 카드 번호가 문장에 한 번만 등장한다는 전제하에.
    for idx, token in enumerate(tokens):
        
        # 카드 브랜드 포함하는지 
        if token in card_brands:
            tags+='B_SS_BRAND '
        
        elif 'ㅇㅇㅇㅇ' in token:
            
            # 카드 번호 시작 부분: 첫 번째 인덱스라면 무조건 B, 
            if num_idx==0:
                tags+='ID_CARD_B '
            
            else:
                tags+='ID_CARD_I '
                
            if opt == 1: # 채워넣기 옵션 O
            
                tokens[idx] = tokens[idx].replace('ㅇㅇㅇㅇ', make_random_number("", 4))
                
            num_idx+=1   
            
        else:
            tags+='O '

            
    # 혹시 모를 중복 공백 제거
    tags = ' '.join(tags.split())
    tokens = ' '.join(tokens)
    f.writerow([tokens, tags])
    
    
def check_card_pattern(input_path):

    order = pd.read_csv(input_path, delimiter='\t', engine='python', encoding='utf-8', names=['SENTENCE', 'TAG'])

    # 카드 번호 패턴: ㅇㅇㅇㅇ ㅇㅇㅇㅇ ㅇㅇㅇㅇ ㅇㅇㅇㅇ 이 등장하는 문장만 추출
    order = order[order['SENTENCE'].str.contains('ㅇㅇㅇㅇ ㅇㅇㅇㅇ ㅇㅇㅇㅇ ㅇㅇㅇㅇ')] # 왜 reset_index를 이 뒤에 바로 붙이면 안 되는지...
    order = order.reset_index(drop=True)
    order = order['SENTENCE']

    # 패턴 중복 제거하기 (set 사용)
    card_pattern = set()
    for i in range(len(order)):
        card_pattern.add(order.iloc[i])
        
    return card_pattern
        
    # print(card_pattern)
    # print("카드번호 등장 패턴 수: ", len(card_pattern)) # 377



                
def tagging(output_file, card_pattern, opt):
    
    '''
    opt == 0: 비식별화 (ㅇㅇㅇㅇ) 유지 & 태깅
    opt == 1: 랜덤으로 생성한 데이터로 대체 & 태깅
    '''
    
    # 등장하는 카드 패턴들만 뽑아서 -> tsv -> 채우기
    with open(output_file, 'w', newline='', encoding='utf-8') as output:
    
        f = csv.writer(output, delimiter='\t')
        
        # for tagging test
        # set_list = list(card_pattern)
        # set_list = set_list[:1]
        
        for line in card_pattern: # set 내에 있는 패턴들
            if line:
                writedata(line, f, opt)
                



def main():
    
    path = './shopping_주문_training_with_o_tag.tsv'
    output_file = './shopping_주문_training_card_pattern.tsv'
    
    card_pattern = check_card_pattern(path)
    tagging(output_file, card_pattern, 1)
    



if __name__ == "__main__":
    main()


