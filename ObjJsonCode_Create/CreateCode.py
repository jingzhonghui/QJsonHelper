import re
class CreateCode:
    def __init__(self,_code):
        self.code = _code
        self.keyWords = ['int','double','float','std::string','std::list','std::vector',
        'std::map','std::unordered_map','std::unordered_set','std::set','bool','char','short','long',
        'string','list','vector','map','unordered_map','unordered_set','set','QString','QList','QVector',
        'QMap','QHash','QSet','QByteArray','QVariant','QVariantList','QVariantMap','QVariantHash','QVariantSet']
    
    def _preProcess(self) -> list:
        if not self.code:
            return []
        #按照换行符分割
        _lines = self.code.split('\n')
        _temp = []
        #去除空行和注释
        for _line in _lines:
            if _line.strip() == '' or _line.strip().startswith('//'):
                continue
            _temp.append(_line)
        _lines = _temp
        return _lines
    
    #按照struct分割
    def _splitStruct(self,_code:list) -> list:
        #过滤掉空字符串
        _code = list(filter(lambda x:x.strip() != '',_code))
        return _code
    
    def _create(self,_code:str) -> str:
        _code = _code.strip()
        #匹配结构体名
        _match = re.match(r'(\w+)',_code)
        #没匹配到就直接返回
        if not _match:
            return ''
        #获取到名字
        _structName = _match.group(1)
        #匹配大括号内的内容
        #.*表示匹配除了\n \r之外的字符
        _variable = re.findall(r'(?<=\{)(.*)(?=\})',_code,re.S)
        if not _variable:
            return ''
        _temp = _variable[0].split(';')
        _tempList = []
        for _var in _temp:
            _var = _var.strip()
            if not _var:
                continue
            _tempList.append(_var)

        #获取变量类型和变量名
        _variableList = []
        for _var in _tempList:
            _tt = _var.split(' ')
            _tt = list(filter(lambda x:x.strip() != '' and not x.strip().startswith('//'),_tt))
            if len(_tt) != 2:
                continue
            _variableList.append(_tt)
        
        
        return self._joinCode(_structName,_variableList)
        
    #拼接代码
    def _joinCode(self,_name:str,_variable:list) -> str:
        _result = []
        _result.append(f'#include "JsonHelper.h"')
        _result.append(f'class {_name}: public QObject')
        _result.append(r'{')
        _result.append(f'\tQ_OBJECT')
        #声明属性
        for _var in _variable:
            _result.append(f'\tQ_PROPERTY({_var[0]} {_var[1]} READ READ_FUNC_NAME({_var[1]}) WRITE WRITE_FUNC_NAME({_var[1]}) CONSTANT)')

        _result.append(r'public:')
        #拷贝函数
        _result.append(f'\t{_name} &operator=(const {_name}& other)')
        _result.append('\t{')
        _result.append('\t\tif(this != &other)')
        _result.append('\t\t{')
        for _var in _variable:
            _result.append(f'\t\t\tthis->{_var[1]} = othre.{_var[1]};')
        _result.append('\t\t}')
        _result.append('\t\treturn *this;')
        _result.append('\t}')
        #声明变量
        for _var in _variable:
            _result.append(f'\t{_var[0]} {_var[1]};')

        _result.append(r'protected:')
        for _var in _variable:
            #判断是否为基础类型
            _index = _var[0].find('<')
            _tempName = _var[0]
            if _index != -1:
                _tempName = _tempName[:_index]
            if _tempName in self.keyWords:
                _result.append(f'\tREAD_WRITE_VALUE({_var[0]},{_var[1]})')
            else:
                _result.append(f'\tREAD_OBJECT({_var[0]}')
                _result.append(f'\tWRITE_OBJECT({_var[0]}')
        
        _result.append(r'};')
        return '\n'.join(_result)

    def run(self) -> str:
        _lines = self._preProcess()
        if not _lines:
            return ''
        _temp =  '\n'.join(_lines)
        _lines = self._splitStruct(_temp.split('struct'))

        _result = []
        for _line in _lines:
            _temp = self._create(_line)
            if not _temp:
                continue
            _result.append(_temp)

        return '\n'.join(_result)
    
