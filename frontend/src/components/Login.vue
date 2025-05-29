<template>
    <!-- 全屏背景容器 -->
    <div class="background">
        <div class="content">
            <!-- 顶部Logo+标题区域 -->
            <div class="introduction">
                <img :src="require('../assets/TeachingCode.png')" class="logo" :class="{ 'small-logo': isCollapse }">
                <span class="logotext">编程教育多智能体系统</span>
            </div>

            <!-- 登录表单主容器 -->
            <div class="login-container">
                <!-- 表单内容容器 -->
                <div class="form-content">
                    <!-- 手机号输入 -->
                    <div class="input-group">
                        <input type="text" class="input-field" placeholder="请输入用户名/手机号/邮箱地址">
                    </div>

                    <!-- 密码输入 -->
                    <div class="input-group">
                        <input type="password" class="input-field" placeholder="请输入密码">
                    </div>

                    <!-- 主操作按钮 -->
                    <button class="primary-btn" @click="handleLogin">登录</button>

                    <!-- 底部链接区域 -->
                    <div class="action-links">
                        <a href="#" class="link left-link">忘记密码</a>
                        <a href="#" class="link right-link">立即注册</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'WhiteThemeLogin',
    methods: {
        handleLogin() {
            // 这里可以添加登录验证逻辑
            this.$router.push('/main')
        }
    }
}
</script>

<style scoped>
/* 全屏背景容器样式 */
.background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: #000;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transform: translateY(-5%);
    min-height: 100vh;
    padding: 20px;
}

.introduction {
    display: flex;
    margin-bottom: 12px;
}

.logo {
    width: 80px;
    height: 60px;
}

.logotext {
    color: #4d6bfe;
    margin-left: 15px;
    font-size: 30px;
    font-weight: bold;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

/* 登录表单主容器 */
.login-container {
    width: 370px;
    background: #1a1a1a;
    border: 1px solid rgba(255, 255, 255, 0.1);
    /* 半透明边框 */
    border-radius: 18px;
    padding: 40px;
    margin-top: 20px;
}

/* 表单内容容器 */
.form-content {
    display: flex;
    flex-direction: column;
    gap: 25px;
    /* 元素垂直间距 */
}

/* 输入框样式 */
.input-group {
    width: 100%;
    display: flex;
}

.input-field {
    width: 100%;
    height: 45px;
    padding: 0 16px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    /* 半透明边框 */
    border-radius: 10px;
    font-size: 15px;
    background-color: #1a1a1a;
    color: #fff;
}

.input-field:focus {
    border-color: #4d6bfe;
    color: #fff;
}

/* 主按钮样式 */
.primary-btn {
    width: 100%;
    height: 45px;
    background: #4d6bfe;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 15px;
    cursor: pointer;
}

.primary-btn:hover {
    opacity: 0.8;
}

/* 底部链接区域 */
.action-links {
    display: flex;
    justify-content: space-between;
}

.link {
    font-size: 14px;
    text-decoration: none;
    transition: color 0.3s;
}

.left-link {
    color: #6780fe;
}

.right-link {
    color: #6780fe;
}

.link:hover {
    opacity: 0.8;
}
</style>