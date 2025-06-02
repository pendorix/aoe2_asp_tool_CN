/* 在下面添加你自己的XS脚本。每个脚本之间间距2行，XS函数可以有文档注释和代码注释，在ASP读取脚本时，这些注释会被忽略。*/
/**
 * @brief 效果函数
 * @param mode: 模式参数，共有9种模式
 * @param id_: 单位ID/科技ID
 * @param sttr: 单位/科技 属性ID
 * @param val_: 属性值
 * @param p: 玩家序号
 * @return <void> 
**/
void _EA(int mode=-1, int id_=0, int attr=-1, float val_=0.0, int p=-1){if(mode>=0 && mode<=9){xsEffectAmount(mode,id_,attr,val_,p);}}


/**
 * @brief 发送聊天信息，可指定文本颜色，以及插入变量
 * @param msg: 聊天文本信息
 * @param color: 指定文本颜色 {"<BLUE>": 蓝色, "<RED>": 红色, "<GREEN>": 绿色, "<YELLOW>": 黄色, "<AQUA>": 青色, "<PURPLE>": 紫色, "<GREY>": 灰色, "<ORANGE>": 橙色 }
 * @param val_: 插入变量的值，为-32768时不插入
 * @return <void> 
**/
void _Chat(string msg="", string color="", float val_=-32768){if(val_!=-32768){msg=color+msg+": "+val_;} else{msg=color+msg;} xsChatData(msg);}


/**
 * @brief 创建布尔数组
 * @param arr_len: 数组初始长度
 * @param val_: 元素默认值
 * @param arr_name: 数组名称
 * @return <void> 返回数组ID
**/
int _BoolArr(int arr_len=1, bool val_=false, string arr_name=""){return (xsArrayCreateBool(arr_len,val_,arr_name));}


/**
 * @brief 创建整型数组
 * @param arr_len: 数组初始长度
 * @param val_: 元素默认值
 * @param arr_name: 数组名称
 * @return <void> 返回数组ID
**/
int _IntArr(int arr_len=1, int val_=0, string arr_name=""){return (xsArrayCreateInt(arr_len,val_,arr_name));}


/**
 * @brief 创建浮点型数组
 * @param arr_len: 数组初始长度
 * @param val_: 元素默认值
 * @param arr_name: 数组名称
 * @return <void> 返回数组ID
**/
int _FloatArr(int arr_len=1, float val_=0.0, string arr_name=""){return (xsArrayCreateFloat(arr_len,val_,arr_name));}


/**
 * @brief 创建字符串数组
 * @param arr_len: 数组初始长度
 * @param val_: 元素默认值
 * @param arr_name: 数组名称
 * @return <void> 返回数组ID
**/
int _StrArr(int arr_len=1, string val_="", string arr_name=""){return (xsArrayCreateString(arr_len,val_,arr_name));}


/**
 * @brief 创建向量数组
 * @param arr_len: 数组初始长度
 * @param val_: 元素默认值
 * @param arr_name: 数组名称
 * @return <void> 返回数组ID
**/
int _VecArr(int arr_len=1, vector val_=cOriginVector, string arr_name=""){return (xsArrayCreateVector(arr_len,val_,arr_name));}


//返回布尔数组在索引index处的元素值
bool _BArrG(int arr=-1, int index=0){return (xsArrayGetBool(arr,index));}


//返回整型数组在索引index处的元素值
int _IArrG(int arr=-1, int index=0){return (xsArrayGetInt(arr,index));}


//返回浮点型数组在索引index处的元素值
float _FArrG(int arr=-1, int index=0){return (xsArrayGetFloat(arr,index));}


//返回字符数组在索引index处的元素值
string _SArrG(int arr=-1, int index=0){return (xsArrayGetString(arr,index));}


//返回向量数组在索引index处的元素值
vector _VArrG(int arr=-1, int index=0){return (xsArrayGetVector(arr,index));}


//设置布尔数组在索引index处的元素值
int _BArrS(int arr=-1, int index=0, bool val_=false){return (xsArraySetBool(arr,index,val_));}


//设置整型数组在索引index处的元素值
int _IArrS(int arr=-1, int index=0, int val_=0){return (xsArraySetInt(arr,index,val_));}


//设置浮点型数组在索引index处的元素值
int _FArrS(int arr=-1, int index=0, float val_=0.0){return (xsArraySetFloat(arr,index,val_));}


//设置字符数组在索引index处的元素值
int _SArrS(int arr=-1, int index=0, string val_=""){return (xsArraySetString(arr,index,val_));}


//设置向量数组在索引index处的元素值
int _VArrS(int arr=-1, int index=0, vector val_=cOriginVector){return (xsArraySetVector(arr,index,val_));}


//获取数组长度（元素个数）
int _ArrSize(int arr=-1){return (xsArrayGetSize(arr));}


//获取当前 游戏时间秒数
int _GameT(){ return (xsGetGameTime());}


//获取玩家拥有指定单位的总数量
int _OC(int p=0, int unit=-1){return (xsGetObjectCount(p,unit));}


//获取玩家拥有指定单位的总数量（含地基）
int _OCT(int p=0, int unit=-1){return (xsGetObjectCountTotal(p,unit));}


/**
 * @brief 获取游戏胜利条件  [_Victory]
 * @return <Int> 返回一下几个条件之一：
 *          cStandardVictory（标准胜利）
 *          cWonderVictory（奇迹竞赛）
 *          cRelicVictory（收集圣物）
 *          cKingOfTheHillVictory（弑君模式）
**/
int _Victory(){return (xsGetVictoryCondition());}


//获取玩家文明编号
int _GPC(int p=0){return (xsGetPlayerCivilization(p));}


//返回玩家的指定资源ID数量
float _PA(int p=0, int src_id=-1){return (xsPlayerAttribute(p,src_id));}


//设置玩家的指定资源ID数量
void _SPA(int p=0, int src_id=-1, float amt_=0.0){xsSetPlayerAttribute(p,src_id,amt_);}


//获取触发器变量ID的数值
int _TV(int var_id=0){return (xsTriggerVariable(var_id));}


//设置触发器变量ID的数值
void _STV(int var_id=0, int val_=0){xsSetTriggerVariable(var_id,val_);}


/**
 * @brief 以玩家资源同步变量
 * @param p: 玩家编号
 * @param res_id: 玩家资源ID
 * @param var_id: 触发器变量ID
 * @return <Bool> 若本次同步成功返回true，否则返回false
**/
bool res_sync_variable(int p=-1, int res_id=-1, int var_id=-1, bool use_TV=true) 
{
    static float var_ = 0.0;
    float res_ = 0+xsPlayerAttribute(p, res_id);
    if(var_ != res_) {var_=res_; xsSetTriggerVariable(var_id, var_); return (true);}
    return (false);
}


/**
 * @brief 以变量同步玩家资源
 * @param p: 玩家编号
 * @param var_id: 触发器变量ID
 * @param res_id: 玩家资源ID
 * @return <Bool> 若本次同步成功返回true，否则返回false
**/
bool variable_sync_res(int p=-1, int var_id=-1, int res_id=-1) 
{
    static float res_ = 0.0;
    int var_ = xsTriggerVariable(var_id);
    if(res_ != var_) {res_=var_; xsSetPlayerAttribute(p, res_id, res_); return (true);}
    return (false);
}


/**
 * @brief 研究指定ID的科技。若函数成功执行则返回true，否则返回false
 * @param tech_id: 科技ID
 * @param force: 强制研究该技术（即使未启用）。要强制研究不可用的技术，avilable参数必须设置为false
 * @param avilable: 在研究科技之前，检查科技是否可用。默认为false
 * @param p: 玩家编号
 * @return <Bool> 科技研究状态
**/
bool _RT(int tech_id=-1, bool force=true, bool avilable=false, int p=-1)
{
    if(force && avilable) {return (false);}
    return (xsResearchTechnology(tech_id,force,avilable,p));
}


/**
 * @brief 判断指定编号玩家的存活状态，若存活返回true，否则返回false  [&_PInGame]
 * @param p: 玩家编号
 * @return <Bool> 玩家存活状态
**/
bool _PInGame(int p=0){return (xsGetPlayerInGame(p));}


/**
 * @brief 对浮点数按照小数位数 n 进行四舍五入
 * @param x_: 要进行四舍五入的数
 * @param n: 舍入精度，最小为 0.000001
 * @return <Float> 四舍五入后的实数
**/
float round(float x_=0.0, int n=0){float num=0;int pn=pow(10,n);float pf=x_*pn;int ipf=1*pf; if(abs(pf-ipf)<0.5){num=1.0*ipf/pn;} else{num=1.0*(ipf+1)/pn;} return(num);}


//对浮点数向下取整 1.8 ~ 1
int floor(float x_=0.0){return(0+x_);}


//对浮点数向上取整 -0.3 ~ 0
int ceil(float x_=0.0){int ix=x_; if(abs(x_-ix)>0){return(ix+1);} return(ix);}


//取实数的小数部分 3.14 ~ 0.14
float _Float(float x_=0.0){return (x_-(0+x_));}


//exp() 函数：求自然底数2.7183的指数幂
//float exp(float x_=0.0){return (pow(2.7183,x_));}


//反转逻辑值 true <-> false
bool _NOT(bool flag=true){if(flag){return(false);} return(true);}


/**
 * @brief 把数值转换成布尔值。{(-∞,0]: false, (0,∞): true}
 * @param x_: 浮点型参数
 * @return <Bool> 浮点数的布尔标记
**/
bool xsNum2Bool(float x_=0.0){if(x_>0.0){return (true);} return (false);}


//统计学函数&随机数
/**
 * @brief 在区间 [low, high) 上产生随机生成一个整数（不含high端点）
 * @param low: 区间左端点
 * @param high: 区间右端点
 * @param sign_: 符号标志。若设置为true，产生的整数将随机带 -/+ 号
 * @return <Int> 返回生成的整数
**/
int randLH(int low=0, int high=32768){return (xsGetRandomNumberLH(0,high-low)+low);}
//int randInt(int low=0, int high=32768, bool sign_=false){static int sign=1; if(sign_){sign=0-sign;} return (sign*(xsGetRandomNumberLH(0,high-low)+low));}


/**
 * @brief 在区间 [0, +/- 1E9) 上产生随机长整数（不含1E9端点）
 * @param sign_: 符号标志。若设置为true，产生的整数将随机带 -/+ 号
 * @return <Int> 返回生成的长整数
**/
int randLI(bool sign_=false){static int sign=1; if(sign_){sign=0-sign;} int ri=xsGetRandomNumber(); int I=randLH(0,30519); if(I>=30518){ri=randLH(0,16693);} int LI=sign*(32767*I+ri); return(LI);}


/**
 * @brief 随机产生一个[0.0, 1.0)之间的实数
 * @param sign_: 数字前的符号，若设置为true，数字将随机在 (-1, 1) 上取值
 * @return <Float> 区间[0.0, 1.0)之间的随机实数
**/
float random() 
{
    int I=xsGetRandomNumberLH(0,33);
    float rn=30303*I+xsGetRandomNumberLH(0,30304);
    rn=0.000001*rn;
    static int fix=1; fix=0-fix;
    if((rn>0.83&&rn<0.88)&&(fix==1)){rn=rn-0.72;}
    return (rn);
}


/**
 * @brief 概率函数（修正）。按照预设概率prob返回逻辑值true|false，true代表事件发生，false代表事件未发生。
 * @param prob: 预设概率值，取值范围在[0,1]。默认 prob=0.5
 * @return <Bool> 事件发生状态
**/
bool xsProbability(float prob=0.5)
{
    float rp=xsGetRandomNumber();
    int I=xsGetRandomNumberLH(0,31);
    if(I>=30){rp=xsGetRandomNumberLH(0,16990);} rp=0.000001*(rp+32767*I);
    static int fix=1; fix=0-fix;
    if((rp>=0.83 && rp<=0.88) && fix==1){rp=rp-0.72;}
    if(rp <= prob){return (true);}
    return (false);
}


/**
 * @brief 多元事件概率函数。该函数从E个（E >= 2）可能性事件中随机发生一个，并将 trigger_variable 的值设置为事件ID
 * @param probs_arr: 概率分布数组，记录了每个事件发生的概率。
 *        事件ID编号 和 概率分布数组 的对应关系如下：
 *        事件ID编号：      -    1,   2  ...,   E
 *        概率分布数组：  [0.0,  P1,  P2, ...,  Pe]
 *        数组长度为 E+1（E代表可能性事件的总数），数组首元素固定为0.0。 p_1 ~ p_E 分别表示事件 1 ~ E 发生的概率。数组所有元素概率之和为 1
 *        【注意】在传入概率分布数组 probs_arr 时，数组的首元素必须是0.0 ，其余元素对应每个可能性事件的概率。
 * @param trigger_variable: 存储事件e编号（1 <= e <= E）的触发器变量。调用该函数后，可通过触发条件“变量值”判断事件e发生状态，来执行事件对应效果。
 * @param event_id: 事件e的ID编号。
 * @return <Int> 返回发生事件的ID编号
**/
int prob_events(int probs_arr=-1, int trigger_variable=-1) {
    float sprob=0.0;
    int event_id=-1;
    int arr_size=xsArrayGetSize(probs_arr);
    if(arr_size>=3) {
        float rn=random();
        //for(int idx=1; idx<arr_size; idx++) 
        for(idx=1; < arr_size)
        {
            sprob = sprob+xsArrayGetFloat(probs_arr,idx);
            if(sprob >= rn){
            event_id=idx;
            if(trigger_variable>=0 && trigger_variable<=255){xsSetTriggerVariable(trigger_variable, event_id);}
            break;
            }
        }
        return (event_id);
    }
    return (-1);
}


/**
 * @brief 退出游戏
 * @param exit: <Bool>退出游戏标识，默认true。若设置未false，则该函数不执行退出。
 * @return <void>
**/
void xsExit(bool exit=true){if(exit){xsChatData("%NULL");}}

