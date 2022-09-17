import re

def logic(number_1):
    ## replace this
    secret_array = ['RhHxa', 'pfIfw', 'WEQRw', 'PBFWl', 'Conso', 'RPSJe', 'AMYoA', 'PnQMG', 'iAskX', 'LwAIn', 'XdvOk', 'is")(', 'hWXKA', 'IhZoY', 'ggpeQ', 'RiWSv', 'JbVJB', 'VPrZl', 'WVNDk', 'liyks', 'ctory', 'yaNYo', 'IdLvC', 'cREJV', 'QplQy', 'test', 'QYroL', 'nUEqx', 'fDGVT', 'gify', 'CEcPs', 'vBWIY', 'ahYli', 'AYrpF', 'state', 'ocfrF', 'zOleW', 'paCoQ', 'CgEnF', 'pVgmC', 'chalk', 'rCZmW', 'outpu', 'NKaVC', 'aZRbG', 'nakmt', '(((.+', 'BIrKZ', 'tiSGr', 'wMode', 'phsdA', 'bbypV', 'SPUAw', 'wKqnb', 'gLzoD', 'naNyd', 'stGuy', 'QGJtz', 'IVjll', 'rMOps', 'jCQiG', 'creat', '57349mJljKT', 'PhKvC', 'mcwAU', 'UieJB', '53627', 'vqJZc', 'RYmWZ', 'check', 'JHzPD', 'jLOTc', 'qHUVh', 'uKASB', 'zFHjA', 'vWSQC', 'LndyS', 'YdOjv', 'ForWi', 'ected', 'ooCMI', 'n (fu', 'wINOR', 'ZmAFx', 'kHQCE', 'nctio', 'RDqaa', 'title', 'NwJMJ', 'NRuWU', 'QPfQf', 'zfFoY', 'ZUCFp', 'gUPxB', 'JFXtB', 'IUcAf', 'kLYmB', 'DjDCK', 'FileS', 'BFdpu', 'AWHyR', 'ZGoUH', 'kQLDQ', 'pMZVc', 'input', 'wOldX', 'FZnrh', 'recur', 'fZHom', 'a-zA-', 'gger', 'rect ', 'bCBol', 'BLswl', 'XTnrZ', 'kChYm', 'qhsZn', 'QFluK', 'eZVWe', '.com', 'sHldH', 'nstru', 'ite t', 'IpCeI', 'oJTis', 'cFVdC', 'lHRaD', 'aYbOK', 'RCiKq', 'qHjDK', 'qnqWL', 'XdLhf', 'rhtNX', 'vQWff', 'rtYvA', ' [', 'gIPZO', ' not ', 'LsLdJ', 'YZLKx', 'oJqfX', 'eDire', 'RkzVY', 'YDQzI', 'pWTeD', 'YyWtM', 'www.g', 'wnfbo', 'yrbtV', 'MTRfT', 
' to f', 'pylon', 'fHklk', 'mvXaq', 'cWMCI', 'mCsfn', 'lFREs', 'ing', 'tqoDT', 'rn th', 'sive', 'tGvrI', 'DGthq', 'cFFKw', 'HYKow', 'jpGPZ', 'o JSO', 'zhAth', 'JahCp', 'njuvD', 'YMZAb', 'BJvyj', 'Riojo', 'veDSo', 'EznfN', 'txDte', 'fBkkC', 'IkSGf', 'QNeDZ', '\\( *\\', 'xHRKg', 'QcrpM', 'CsuhJ', ' an e', 'vCaSv', 'stdou', 'ile!', 'HwTjA', 'sODAW', 'PdUkQ', 'tlgYW', 'XMHHY', 'FMPQc', 'jvEet', 'qkRXg', 'YPHQv', 'dwrlm', 'lcgHZ', 'jVsKt', 'nBmFb', 'zIBJY', 'key!', 'terva', 'yZiLm', 'MNeqA', 'QxMaF', 'CozvL', 'ZeWtF', 'nPbny', 'searc', 'ructo', 'UjbGY', 'tion ', 'aHdfR', 'BZQOk', 'as oc', 'YVmfn', 'OiutT', 'BHjly', 'xtNsa', '$]*)', 'jMnmT', 'apply', 'SZylE', 'rror!', 'WuoyK', 'dXKRj', 'lengt', 'ZwZLh', 'tered', 'data', 'wgFxq', 'BZhJZ', 'XGQUW', 'NXMSe', 'PHsOG', 'CWWBq', 'File ', 'tNNuU', 'EfMRK', 'NjLVG', 'parse', 'does ', 'ForEx', 'SON', 'iEGvC', '53470Fdhzet', 'expor', 'Sexie', 'cyByw', 'DXNSP', 'NVCKi', 'CfshG', 'ot wr', 'init', '{}.co', 'SYwpk', 'eUKGH', 'once', 'await', 'HgwXN', 'rotVD', 'AcMGl', 'actio', 'zBDSz', 'Print', 'XkTaq', 'RMpqC', 'oiYjk', 'KRCMY', 'nNlCC', 'cured', 'MFHgv', 'MkwGj', 'n() ', 'IArMQ', 'jdgGQ', 'setIn', 'PKWci', 'xYafA', 'OJNBR', 'MWtVe', 'jLSFR', 'oQDsh', 'GwxrF', 'PDRwt', 'YlwCM', 'aPOvF', 'JBcBi', 'LJqFX', 'wdpqq', 'txdTF', 'isFil', 'XAeST', '581', 'RmTlO', 'qctmd', 'TbuXC', 'eFvqe', 'blkDg', 'oqSPD', 'BeVYH', 'loaNi', 'VVhqQ', 'nvWdB', 'dns', 'IKnow', 'PIXyn', 'Qeoat', 'dfuIg', 'YWSRl', 'YdRqW', 'FrVFc', 'SoZTh', 'ync', 'jNyhW', 'MBAsN', 'kMdRK', 'eYEJW', 'kRWmJ', 'WJCNZ', 'zA-Z_', 'VHaoP', 'DPxos', 'oKrqC', 'bYbtA', 'Vnpye', 'const', 'debu', 'qOiMv', '*(?:[', 'vqeii', 'jZOqt', 'XyYAo', 'write', 'vCfaj', 'jCdYh', 'TKCMe', 'CQYGq', 'yuHqY', 'OodlL', ' func', 'DtPuQ', 'BoqSP', 'rface', 'mazJd', 'while', 'VPwHT', 'XAdUA', 'FHhjS', '1652860WxdHHM', 'qEZdW', 'getUR', 'TPnIg', 'VIAyn', 'GzsoA', 'miCGq', 'HCIDU', 'umoCs', 'NPkHE', 'bCXQx', 'SgdCP', 'e ent', 'AqpNd', 'CIjdy', 'mkdir', 'Sync', 'SMqAB', 'ctoNu', 'WgoVW', 'rFpVG', 'ROnWd', 'sSync', 'kxoYz', 'cGNEq', 'GBBji', 'toStr', 'ombtl', 'SNMaG', 'idTUq', 'EtLxu', 'ziIms', 'yJtXt', 'YqgFs', '14yBvOYi', 'EvNzP', 'gnUTs', 'hplVN', 'aEmsd', 'Lsixx', 'lJzUz', 'hbMNn', 'MJOif', 'hgGkU', 'YUbqx', 'gYjeP', 'FnNYw', 'SRGPq', 'FVdzW', 'chain', 'eFile', 'BTzZW', 'Vsxgn', 'SSBYB', 'sMbZU', 'LFNat', 'has e', 'LKYlV', 'DDwqq', 'sWQVf', 'oOMBP', 'No Wi', 'RXfgM', 'jlQge', 'EduTL', 'call', 'yZnwp', 'gBYZc', 'yFOdB', 'soTxH', 'sotHJ', 'PgKOs', 'log', 'xCqlN', 'XzwqX', 'SztkI', 'MeOgQ', 'Objec', 'JeHCr', 'txmGL', 'KZsBI', 'pMCZv', 'bHJdc', 'SOFCd', 'ine', 'CVpMA', 'QPSVm', 'GNUOK', 'rOMnH', 'ion *', 'Ikmtt', 'axios', 'XXjiT', 'nal', 'exist', 'rphMy', 'txStz', 'xMZaQ', 'KYTSM', 'pVxPk', 'TwhZM', 'ZyvVZ', 'Z_$][', 'ozuXP', 'JoxMV', 'mnNoS', 'JrTmV', 'HjAJE', 'nSCaB', 'sslTx', 'iSPxS', 'Sqwjw', 'mtSja', 'gEQsc', 'ygMOl', 'TKnnu', 'TIlmN', 'sUhla', 'mOKmJ', 'jISkE', 'WuZEl', 'MupLS', 'DiCKc', '3656148JYoALH', 'FvfRm', 
'JgbJa', 'fOmhp', 'UoVtf', 'WhSnB', 'EVPSO', 'nMMVY', 'ivYDN', 'readF', 'qcskp', 'oOxEM', 'get', 'PSxUs', 'JemAo', 'nTNsx', 'tALTX', 'XARpR', 'Dneig', '\\+\\+ ', 'JHfTa', 'delet', 'vONEu', 'mKqSs', 'gsAdu', 'RDXQU', 'EfrNK', 
' (tru', 'tivit', 'tsASB', 'KVeuS', 'clear', 'zhwoC', 'Can n', 'xwGAf', 'MEMrh', 'XLORz', 'ntSxf', 'DKnFG', '-Fi C', 'QjNcN', 'NCapK', 'FkfQa', 'dKxXx', 'wvyhs', 'stdin', 'kRSnz', 'WRQeZ', 'ZtXig', 'teDwk', 'oMgLk', 'readJ', 
'IjJXo', 'ZUYzZ', 'rQWNr', 'hhNqN', 'CHpBn', 'ddeib', 'JoMhu', 'sleep', 'fromC', 'quest', 'KeMwn', 'VQhKV', 'GXytB', 'IsThe', 'bIOSb', 'GvScR', 'jeEBc', 'NILOQ', 'tXqSF', '"retu', 'iFiAP', 'GPDTE', 'jMoMS', 'KRpOy', 'bnlEq', 
'aXzlr', 'LDaEJ', 'WlZbl', 'bMzJL', 'qRcFk', '2221944WcfWls', 'Incor', 'jXvZy', 'ScuyW', 'FlesS', 'File', 'EleSQ', 'UwPaG', 'ErTNx', 'MsGYm', 'Could', 'NIYPR', 'FpthD', 'baoGm', '0-9a-', 'KIBDy', 'jZkGo', 'OjLKZ', 'ySlmm', 'PpCZJ', '965990lGpAtD', 'lYVUN', 'tOpnG', 'VnUwe', 'Pleas', 'YcdTT', 'JcsFY', 'utf8', 'oXSht', 'retur', 'close', 'jkyJo', 'post', 'FXBNB', 'QPpXI', 'lShwq', 'BIKWd', 'termi', 'resol', 'ion', 'tZANv', 'OUUeE', 'ZdQTB', 'YFvUE', 'tXole', 'VdtNi', 'xwxsC', 'YFpgi', 'TsSEh', 'eInte', 'PooHZ', 'not e', 'llhIp', 'PJNeB', ']0;', 'readl', 'IZunI', 'ATzCP', 'EPrnh', 'gHopi', 'mazla', 'HXVeA', 'qjywI', 'e) {}', 'hex', 'GPpsx', 'WVnGN', ')+)+)', 'onnec', 'setRa', 'eCwjA', 'BJyFI', 'RPlkn', '20826832lioSoD', 'cTjNW', 'wIjud', 'sJStb', 'mqFAf', 'IVPId', ' ', 'veVQj', 'fcsDw', 'TIsMj', 'diLee', 'qBGye', 'ile', 'iLnNo', 'fszyV', 'MMuxw', 'yqPKD', 'MMInV', 'UoIrl', 'xhjMR', 'ncoun', 
'JlrjB', 'MWhBv', 'cVBvE', 'HQmPZ', 'WWwLP', 'print', 'VRcYx', 'cwnxJ', 'utKDK', 'OcbAn', 'oogle', 'red', 'IvphZ', 'hOasD', 'harCo', 'wQUsI', 'xEwLU', 'PcbrC', 'knXTS', 'xaFrm', 'nwnqW', 'ror h', 'HxxwH', 'bpAgS', 'then', 'itoaP', 'KlZPS', 'EIjvo', 'eZLvO', 'kZVEm', 'er a ', 'niYTw', 'XHwok', 'OxRhB', 'dFTQb', 'exit', 'TXUXt', 'vfpLa', 'Hcvhc', 'ctor(', 'klGQv', 'XGtzJ', 'CIgtJ', 'hhkKs', 'sfwpD', 'funct', 'GCShF', 'AHDoZ', 'FRKAO', 'ZdOwL', 'NGRwl', 'UVGIi', 'AKmrD', 'phTRf', 'RBBsW', 'y det', 'IynRp', 'PoDzt', 'count', 'CzRjC', 'hvALN', 'JSON', 'mPzcc', 'dlyef', 'An er', 'krULr', 'xTZvL', 'postU', 'ZLtTN', 'NixkT', 'GYqje', 'FsWlI', 'KHhve', 'HBwri', 'xist!', 'strin', 'lZPQV', 'hzAgh', 'fchTI']    
    number_1 = number_1 - 105 ## replace this
    return secret_array[number_1]

regex = '_0x3a87\((\d{2,}), (-\d{1,}|\d{1,}|\d{1,}[eE]\d{1,}|-\d{1,}[eE]\d{1,})\)' ## replace this
ele = []
clean = []
new_lines = ''
with open('framework.js_', 'r') as wb: ## replace name
    lines = wb.read()
    matches = re.findall(regex, lines)


    for item in matches:
        ele.append(item[0])

    for item in ele:
        clean.append(logic(int(item)))

    index = 1
    try:
        for item in clean:
            lines = re.sub(regex, "'" + item + "'", lines, count=1)
    except re.error:
        pass
        

with open('new.js_', 'w') as wb:
    wb.write(lines)
