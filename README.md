## babyrobot

### 目前可使用功能
- 定时发送消息
    - 早晨发送早安问候，相识日子纪念， 天气情况推送
    - 午后发送一则小笑话，开心一刻
    - 晚上发送晚安消息，一张精美图片配一句暖心的话
    
- 智能闲聊
    - 即使自己很忙，也不会让TA孤单，机器人智能恢复，不错过每一个交流瞬间。
    - 支持腾讯智能闲聊，图灵机器人，自带无需注册的青云客机器人。
    
 ### 安装环境
 - Python3.x
 - 依赖库
    - itchat
    - requests
    - BeautifulSoup
    
 ### 使用教程
- 将代码克隆到本地：<pre> <code>git clone https://github.com/jvxiao/babyrobot.git </code></pre></br>
- 配置信息，修改 config.cfg文件。重点是修改TA中的内容，其他功能已配置完成，可根据个人需求DIY.
 <pre><code>
   # 对象,可设置多个（单身狗自动忽略...)
   # 可以填TA备注名，微信昵称，或者微信ID
   TA = ['柯北2', '柯南']</code> </pre>
- 运行微信登入脚本：<pre> <code>python loginwx.py
 </code></pre>
 

 ### 后期版本将推出功能
 - 忙碌状态下消息回复
 - 使用表单对对象进行管理
 - 群聊相关功能
 