<?php
/**
 * индекс.php
 *
 * This is an example of the main page of a website. Here
 * users will be able to login. However, like on most sites
 * the login form doesn't just have to be on the main page,
 * but re-appear on subsequent pages, depending on whether
 * the user has logged in or not.
 *
 * Written by: Jpmaster77 a.k.a. The Grandmaster of C++ (GMC)
 * Last Updated: August 26, 2004
 */
include("include/session.php");
?>

<html>
<head>
<meta charset="UTF-8">
<title>Цирковое Общество Неваляшек</title>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background: linear-gradient(135deg, #1a2a6c, #b21f1f, #1a2a6c);
    color: #fff;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.container {
    max-width: 1200px;
    width: 100%;
    margin-top: 50px;
}

header {
    text-align: center;
    margin-bottom: 40px;
}

h1 {
    font-size: 3.5rem;
    margin-bottom: 15px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    background: linear-gradient(to right, #ff8a00, #da1b60);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 1.2rem;
    color: #e0e0e0;
    max-width: 600px;
    margin: 0 auto 30px;
    line-height: 1.6;
}

/* Navigation Styles */
.navbar {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    padding: 0 20px;
    margin: 0 auto 50px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    max-width: 1000px;
}

.menu {
    display: flex;
    list-style: none;
    position: relative;
}

.menu li {
    flex: 1;
    text-align: center;
    position: relative;
}

.menu li a {
    display: block;
    color: white;
    text-decoration: none;
    padding: 20px 25px;
    font-weight: 500;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    position: relative;
    z-index: 1;
}

.menu li a:hover {
    color: #ff8a00;
}

.menu li a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 4px;
    background: linear-gradient(to right, #ff8a00, #da1b60);
    border-radius: 2px;
    transition: width 0.3s ease;
}

.menu li a:hover::after {
    width: 70%;
}

.menu li.active a {
    color: #ff8a00;
}

.menu li.active a::after {
    width: 70%;
}

/* Dropdown Styles */
.dropdown-content {
    display: none;
    position: absolute;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(15px);
    border-radius: 0 0 12px 12px;
    min-width: 200px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    z-index: 100;
    top: 100%;
    left: 0;
    overflow: hidden;
    transform: translateY(10px);
    opacity: 0;
    transition: all 0.4s ease;
}

.dropdown-content a {
    padding: 15px 20px;
    text-align: left;
    display: block;
    color: #fff;
    font-size: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s;
}

.dropdown-content a:hover {
    background: rgba(255, 255, 255, 0.2);
    padding-left: 25px;
    color: #ff8a00;
}

.dropdown:hover .dropdown-content {
    display: block;
    opacity: 1;
    transform: translateY(0);
}

.dropdown > a::after {
    content: '\f107';
    font-family: 'Font Awesome 5 Free';
    font-weight: 900;
    margin-left: 8px;
    font-size: 0.9rem;
}

/* Mobile Menu Button */
.mobile-menu-btn {
    display: none;
    background: transparent;
    border: none;
    color: white;
    font-size: 1.8rem;
    cursor: pointer;
    padding: 10px;
    position: absolute;
    right: 20px;
    top: 10px;
}

/* Content Styles */
.content {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    justify-content: center;
}

.card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 30px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
    background: rgba(255, 255, 255, 0.12);
}

.card h3 {
    color: #ff8a00;
    margin-bottom: 15px;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
}

.card h3 i {
    margin-right: 12px;
    background: linear-gradient(to right, #ff8a00, #da1b60);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card p {
    color: #e0e0e0;
    line-height: 1.6;
    font-size: 1rem;
}

.highlight {
    background: linear-gradient(to right, #ff8a00, #da1b60);
    color: white;
    padding: 2px 5px;
    border-radius: 4px;
}

/* Footer */
footer {
    margin-top: 50px;
    text-align: center;
    padding: 20px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    width: 100%;
    max-width: 1000px;
}

/* Responsive Design */
@media (max-width: 900px) {
    .menu {
        flex-direction: column;
        display: none;
    }

    .menu.show {
        display: flex;
    }

    .mobile-menu-btn {
        display: block;
    }

    .dropdown-content {
        position: static;
        display: none;
        opacity: 1;
        transform: none;
        box-shadow: none;
        background: rgba(0, 0, 0, 0.1);
        border-radius: 0;
    }

    .dropdown:hover .dropdown-content {
        display: none;
    }

    .dropdown.active .dropdown-content {
        display: block;
    }

    .dropdown > a::after {
        content: '\f107';
        float: right;
        transition: transform 0.3s;
    }

    .dropdown.active > a::after {
        transform: rotate(180deg);
    }

    .navbar {
        padding: 15px;
    }

    h1 {
        font-size: 2.5rem;
        margin-top: 20px;
    }
}
</style>
</head>
<body>
    <header>
    <?
        include("nav.php");
    ?>
    </header>
    <div class="content">
    <div class="card">
    <?
    /**
     * User has already logged in, so display relavent links, including
     * a link to the admin center if the user is an administrator.
     */
    if($session->logged_in){
        echo "Добро пожаловать <b>$session->username</b>, вы зашли. <br><br>"
        ."[<a href=\"userinfo.php?user=$session->username\">Мой аккаунт</a>] &nbsp;&nbsp;"
        ."[<a href=\"useredit.php\">Редактировать аккаунт</a>] &nbsp;&nbsp;";
        if($session->isAdmin()){
            echo "[<a href=\"admin/admin.php\">Администрация</a>] &nbsp;&nbsp;";
        }
        echo "[<a href=\"process.php\">Выйти</a>]";
    }
    else{
        ?>

        <h1>Login</h1>
        <?
        /**
         * User not logged in, display the login form.
         * If user has already tried to login, but errors were
         * found, display the total number of errors.
         * If errors occurred, they will be displayed.
         */
        if($form->num_errors > 0){
            echo "<font size=\"2\" color=\"#ff0000\">".$form->num_errors." error(s) found</font>";
        }
        ?>
        <form action="process.php" method="POST">
        <table align="left" border="0" cellspacing="0" cellpadding="3">
        <tr><td>Имя пользователя:</td><td><input type="text" name="user" maxlength="30" value="<? echo $form->value("user"); ?>"></td><td><? echo $form->error("user"); ?></td></tr>
        <tr><td>Password:</td><td><input type="password" name="pass" maxlength="30" value="<? echo $form->value("pass"); ?>"></td><td><? echo $form->error("pass"); ?></td></tr>
        <tr><td colspan="2" align="left"><input type="checkbox" name="remember" <? if($form->value("remember") != ""){ echo "checked"; } ?>>
        <font size="2">Запомнить меня &nbsp;&nbsp;&nbsp;&nbsp;
        <input type="hidden" name="sublogin" value="1">
        <input type="submit" value="Войти"></td></tr>
        <tr><td colspan="2" align="left"><br><font size="2">[<a href="forgotpass.php">Забыли пароль?</a>]</font></td><td align="right"></td></tr>
        <tr><td colspan="2" align="left"><br>Не зарегистрированы? <a href="register.php">Зарегистрироваться!</a></td></tr>
        </table>
        </form>

        <?
    }
    ?>
    </div>
    <div class="card">
    <h3><i class="fas fa-sitemap"></i> Главная страница</h3>
    <p>Мы - цирковое общество неваляшек!</p>
    <p>Занимаемся исследованиями, связанными с циркологией и неваляшководством. Сейчас наш главный проект - гигантская цирковая неваляшка.</p>
    </div>
    <div class="card">
    <h3><i class="fas fa-sitemap"></i> Логотип</h3>
    <img src="/graphics/logo.png" />
    </div>
    <footer>
    <p>Цирковое общество неваляшек &copy; 2007</p>
    </footer>
    </div>
</body>
</html>
