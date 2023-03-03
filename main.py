import os,re,requests

title_level = -1 # 大纲等级
title_name = '' # 标题名称
code_level = False
res_path = os.path.join(os.getcwd(),'res')
md_files = []
headers = {
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
          }

# proxies = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}

def check_picture(s):
    pic_pattern = re.compile(r"\!\[.*\]\(.*\)")
    if re.search(pic_pattern,s):
        return True
    else:
        return False

def check_link(s):
    url_pattern = re.compile(r"((http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)")
    urls = re.findall(url_pattern,s)
    if len(urls)>0:
        return urls[0]
    else:
        return None

def update_level(per_line):
    global code_level,title_level,title_name
    per_line = per_line.strip()
    if len(per_line) == 0:
        return
    else:# 小于0的情况不存在
        if len(per_line)-len(per_line.replace('`','')) ==3 and per_line[0]=='`':
            if len(per_line.replace('`','')) > 0:
                code_level = True
            else: # 我就不信这还会识别错？
                code_level = False
        if per_line[0] == '#' and code_level == False:
            title_name = per_line.replace('#','').strip()
            title_level = len(per_line) - len(title_name)
            return
    pass


def message_logger(number,file_name,line,reason,title_name):
    line = line.replace('\n','')
    return '{0}-{1}:{2}-{3} ({4})'.format(number,file_name,title_name,line,reason)

if __name__ == '__main__':
    # for root,dirs,files in os.walk(res_path):
        # for file in files:
            # if file.endswith('.md'):
                # md_files.append(os.path.join(root,file))
    md_files=['/home/cherry/Projects/picture_checker/res/Docker笔记/Docker容器技术.md']
    for index,element in enumerate(md_files):
        index = index+1
        with open(element,'r') as file,open('log.txt','a') as logfile:
            for line_number,per_line in enumerate(file,start=1):
                    per_line.replace('\n','')
                    update_level(per_line)
                    if check_picture(per_line):
                        url = check_link(per_line)
                        if url == None:
                            logfile.write((message_logger(line_number,os.path.basename(element),per_line,'路径错误',title_name)+'\n'))
                        else:
                            try:
                                request_code = requests.get(url[0],timeout=10,headers=headers).status_code
                                if request_code == requests.codes.ok:
                                    print(message_logger(line_number,os.path.basename(element),per_line,'访问成功',title_name))
                                else:
                                    print(message_logger(line_number,os.path.basename(element),per_line,f'访问失败状态{request_code}',title_name)+'\n')
                                    logfile.write(message_logger(line_number,os.path.basename(element),per_line,f'访问失败状态{request_code}',title_name)+'\n')
                            except requests.exceptions.Timeout:
                                print(message_logger(line_number,os.path.basename(element),per_line,'访问超时',title_name))
                                logfile.write(message_logger(line_number,os.path.basename(element),per_line,'访问超时',title_name)+'\n')
                            except Exception:
                                print(message_logger(line_number,os.path.basename(element),per_line,'资源不存在',title_name))
                                logfile.write(message_logger(line_number,os.path.basename(element),per_line,'资源不存在',title_name)+'\n')
            logfile.close()
            file.close()