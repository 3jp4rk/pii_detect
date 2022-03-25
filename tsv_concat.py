from asyncore import write
import pandas as pd
import csv


dest = './data/data_tagged_concat_refined_20220322.tsv'
src = './data/ner_train_address_out_added_20220322.tsv'


src = pd.read_csv(src, delimiter='\t', engine='python', encoding='utf-8', names=['SENTENCE', 'TAG'])
dest = pd.read_csv(dest, delimiter='\t', engine='python', encoding='utf-8', names=['SENTENCE', 'TAG'])
total = pd.concat([src, dest])

output_file = './data/data_added_20220322_before_split_with_all_O.tsv'




# print(total.isnull().sum().sum())
# print(total[total['TAG'].isnull()])

# # 필요없는 태그 제외하고 전부 O


def writedata(sen, tag, f):
    
    tag_list = ['AD_ADDRESS-B', 'AD_ADDRESS-I', 'AD_DETAIL-B', 'AD_DETAIL-I']

    tags = ''
    tag_token = tag.split(' ')

    for t in tag_token:
        if t != 'O':
            if t in tag_list:
                tags+=t+' '
            else:
                tags+='O '
        else:
            tags+=t+' '
            
    sen_ = sen.split(' ')
    
    # sen_ = ' '.join(sen_)
    

    tags = tags.split(' ')
    aaa = ' '.join(aaa.split())
    
    # 토큰 개수 맞는 것만 
    assert(len(sen_) == len(sen_)), print(sen_, tags)
    # tags = ' '.join(tags.split())
    f.writerow([sen, tags])
    
    # f.writerow([aaa, 'O '*a + 'O'])
    # f.writerow([aaa]) # O 태그 없이 그냥 문장만 추출




with open(output_file, 'w', newline='', encoding='utf-8') as output:
    
    f = csv.writer(output, delimiter='\t')
    
    for i in range(len(total)):
        

        line = total.iloc[i]
        sen = line['SENTENCE']
        tag = line['TAG']
        
        writedata(sen, tag, f)








# tag_list = ['AD_ADDRESS-B', 'AD_ADDRESS-I', 'AD_DETAIL-B', 'AD_DETAIL-I']
# tag_frame = total['TAG']

# print(tag_frame[0])

    




# tag_extract = '|'.join(tag_list)

# total = pd.concat([total_data, add_added])

# total_data = total_data[total_data['TAG'].str.contains(tag_extract)]
# add_added = add_added[add_added['TAG'].str.contains(tag_extract)]

# print("취합본 해당 행 수: ", len(total_data))
# print("추가한 데이터 해당 행 수: ", len(add_added))

dest = './data/data_added_20220322_before_split_with_all_O.tsv'

total = pd.read_csv(dest, delimiter='\t', engine='python', encoding='utf-8', names=['SENTENCE', 'TAG'])


total = total.sample(frac=1).reset_index(drop=True)


# train_test_split 비율 8:2
train_len = int(len(total)*0.8)

total_train = total[:train_len]
totla_test = total[train_len:]

print(total.head(5)) # 1017 (addr 태그만)


# total.to_csv('./data_added_20220322_before_split.tsv', sep='\t', na_rep='NaN', index=False, header=False)

total_train.to_csv('./data_added_20220322_train_with_o.tsv', sep='\t', na_rep='NaN', index=False, header=False)

totla_test.to_csv('./data_added_20220322_test_with_o.tsv', sep='\t', na_rep='NaN', index=False, header=False)








# 1404
# addr1 = addr1.iloc[0:1404, :]

# print(addr1.head(5))
# print(addr2.head(5))
# print(card.head(5))

# 104: addr2


'''

tag_list = ['AD_ADDRESS-B', 'AD_DETAIL-B']
tag_extract = '|'.join(tag_list)

total = pd.concat([total_data, add_added])

total_data = total_data[total_data['TAG'].str.contains(tag_extract)]
add_added = add_added[add_added['TAG'].str.contains(tag_extract)]

print("취합본 해당 행 수: ", len(total_data))
print("추가한 데이터 해당 행 수: ", len(add_added))


# 결측행 체크 

# check = total.isnull().sum().sum()
# print("================")
# # print(check)

# print(total[total['SENTENCE'].isnull()])
# print("================")
# print(total[total['TAG'].isnull()])





print(len(total_train))
print(len(totla_test))

print(len(total))



# print(total.head(5))




'''


