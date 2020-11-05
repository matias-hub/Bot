import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sqlite3
from os import system, name
import time
import math
from selenium.webdriver.chrome.options import Options

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def bases_datos():
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Usuaries(
               usuario text,
               contra text,
               tiempo text
               );""")
    conn.commit()
    conn.close()

    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS lista_perfiles(
               perfil text,
               usuario text,
               echo text
               );""")
    conn.commit()
    conn.close()

    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS ajustes(
               usuario text,
               lim_dia_foll INTEGER,
               lim_hora_foll INTEGER,
               lim_dia_unfoll INTEGER,
               lim_hora_unfoll INTEGER
               );""")
    conn.commit()
    conn.close()

    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS ajustes2(
               usuario text,
               Solo_seg text,
               dosres INTEGER,
               mas_de_tantos INTEGER,
               dias INTEGER
               );""")
    conn.commit()
    conn.close()

    conn = sqlite3.connect("Unfollowd.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS seguidos (
        usuario text,
        seguidores text,
        dejado text)""")
    conn.commit()
    conn.close()

    conn = sqlite3.connect("Unfollowd.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS cuando_seguido (
        usuario text,
        seguidores text,
        momento text)""")
    conn.commit()
    conn.close()

    conn = sqlite3.connect("Unfollowd.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS seguidor (
        usuario text,
        seguidores text)""")
    conn.commit()
    conn.close()

def insta_Unfoll(limite_diario, limite_mediahora, actualizar_tablas, usar_seguidores, user, passw,Solo_seg,dosres,masde,dias):

    print('limite_diario: ', limite_diario)
    print('limite_mediahora: ', limite_mediahora)

    if Solo_seg in 'SIsiSi':
        Solo_seg = True
    else:
        Solo_seg = False

    # habre una ventana, loguea y va hacia el perfil
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    browser = webdriver.Chrome('chromedriver', desired_capabilities={'nativeEvents': False, }, options=options)
    url = "https://www.instagram.com/accounts/login/?source=auth_switcher"

    browser.get(url)
    time.sleep(4)
    username = browser.find_element_by_name("username")
    password = browser.find_element_by_name("password")
    username.send_keys(user)
    password.send_keys(passw)
    time.sleep(5)

    if check_exists_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button/div",browser) is True:
        browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button/div").click()
    else:
        browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[3]/button/div').click()

    time.sleep(4)

    # variables globales
    Lim_minutos = limite_mediahora
    Lim_diario = limite_diario
    Hora_inicio = int(time.strftime("%H"))

    # si se necesesita actualizar las tablas
    if actualizar_tablas is True:
        # borra toda la gente que sigue al usuario
        connection = sqlite3.connect("Unfollowd.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM seguidor WHERE usuario=?", (user,))
        connection.commit()
        connection.close()

        # se dirige a la pagina principal del usuario y levanta el numero de segudores
        browser.get('https://www.instagram.com/' + user + '/')
        source = browser.page_source
        seguidores = source.split('<span class="g47SY " title="')[1]
        seguidores = seguidores.split('">')[0]
        seguidores = seguidores.replace(".", "")
        seguidores = seguidores.replace(",", "")
        seguidores = float(seguidores.replace("k", "000"))
        seguidores = math.floor(seguidores)

        saltar_segudores = False
        print(time.strftime("%H:%M"))
        if saltar_segudores is False:
            # habre la lista de seguidores y scrolea hasta el final
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
            time.sleep(3)
            seguidor = []
            esperar = 0
            for i in range(1, seguidores):
                if usar_seguidores is False:
                    browser.get('https://www.instagram.com/' + user + '/')
                    break
                source = browser.page_source
                print('viendo  ' + str(i) + ' de ' + str(seguidores) + ' seguidores')
                auxdata1 = source.split('<a class="FPmhX notranslate  _0imsa " title="')
                auxdata = auxdata1[-20:]
                time.sleep(1)
                for I in range(1, len(auxdata)):
                    seguidor.append(str(auxdata[I]).split('"')[0])
                    seguidor = list(dict.fromkeys(seguidor))
                path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]")
                if check_exists_by_xpath(path, browser) is True:
                    element = browser.find_element_by_xpath(path);
                    browser.execute_script("arguments[0].scrollIntoView(true);", element);
                else:
                    time.sleep(10)
                    esperar = esperar + 1
                if esperar > 10:
                    input('seguir ?')
                    esperar = 0

            # borra los seguidores anteriores

            connection = sqlite3.connect("Unfollowd.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM seguidor WHERE usuario=? ", (user,))
            connection.commit()

            # guarda todos los seguidores
            for i in range(0, len(seguidor)):
                cursor.execute("INSERT INTO seguidor VALUES(?,?)", (user, seguidor[i]))
                connection.commit()
            connection.close()

        # levanta el numero de segudos
        seguidoss = source.split('<span class="g47SY ">')[2]
        seguidoss = seguidoss.split('</span>')[0]
        seguidoss = seguidoss.replace(".", "")
        seguidoss = seguidoss.replace(",", "")
        seguidoss = int(seguidoss.replace("k", "000"))

        # habre la lista de seguidos y scrolea hasta el final
        browser.get('https://www.instagram.com/' + user + '/')
        time.sleep(3)
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(3)
        seguidos = []
        print(time.strftime("%H:%M"))
        esperar = 0
        for i in range(1, seguidoss):
            print('viendo  ' + str(i) + ' de ' + str(seguidoss) + ' seguidos')
            source = browser.page_source
            auxdata1 = source.split('<a class="FPmhX notranslate  _0imsa " title="')
            auxdata = auxdata1[-20:]
            time.sleep(1)
            for I in range(1, len(auxdata)):
                seguidos.append(str(auxdata[I]).split('"')[0])
                seguidos = list(dict.fromkeys(seguidos))
            path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]")
            if check_exists_by_xpath(path, browser) is True:
                element = browser.find_element_by_xpath(path);
                browser.execute_script("arguments[0].scrollIntoView(true);", element);
            else:
                time.sleep(10)
                esperar = esperar + 1
            if esperar > 10:
                input('seguir ?')
                esperar = 0

        # borra los seguidos anteriores
        connection = sqlite3.connect("Unfollowd.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM seguidos WHERE usuario=? AND dejado=?", (user, 'seguido'))
        connection.commit()

        # guarda todos los seguidos corrientes
        connection = sqlite3.connect("Unfollowd.db")
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM cuando_seguido WHERE usuario = ? ", (user,))
        items = cursor.fetchall()

        for i in range(0, len(seguidos)):
            cursor.execute("INSERT INTO seguidos VALUES(?,?,?)", (user, seguidos[i], 'seguido'))
            if seguidos[i] not in items:
                cursor.execute("INSERT INTO cuando_seguido VALUES(?,?,?) ", (user, seguidos[i], "01/01/2001"))
            connection.commit()
        connection.close()
        print(time.strftime("%H-%M"))
    else:
        # si no tiene que actualizar, utiliza los datos de la base
        connection = sqlite3.connect("Unfollowd.db")
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM seguidos WHERE usuario = ? AND dejado = ? ", (user, 'seguido'))
        auxdata = cursor.fetchall()
        seguidor = []
        seguidos = []
        for i in range(0, len(auxdata)):
            seguidos.append(auxdata[i][2])
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM seguidor WHERE usuario = ? ", (user,))
        auxdata = cursor.fetchall()
        connection.close()

        for i in range(0, len(auxdata)):
            seguidor.append(auxdata[i][2])

    # elimina repetidos
    seguidos = list(dict.fromkeys(seguidos))
    print(len(seguidos), seguidos)

    connection = sqlite3.connect("Unfollowd.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM cuando_seguido WHERE usuario =?', (user,))
    perfiles_seguidos = cursor.fetchall()
    connection.close()
    perfiles_seguidos2= []
    for seg in perfiles_seguidos:
        if seg[-1] != '01/01/2001':
            perfiles_seguidos2.append(seg[1])
    for seg in seguidos:
        if seg not in perfiles_seguidos2:
            seguidos.remove(seg)


    # circula entre todos los perfiles que sigue el usuario
    for seg in seguidos:
        browser.get('https://www.instagram.com/' + seg + '/')
        time.sleep(3)

        # levanta cantidad de seguidores
        source = browser.page_source

        if ">Sorry, this page isn't available.</h2>" in source:
            connection = sqlite3.connect("Unfollowd.db")
            cursor = connection.cursor()
            cursor.execute("""  UPDATE seguidos SET dejado =? WHERE usuario=? AND seguidores = ?""",
                           ('Sorry', user, seg))
            connection.commit()
            connection.close()
            continue
        elif "We're working on it and we'll get it fixed as soon as we can.</p>" in source:
            connection = sqlite3.connect("Unfollowd.db")
            cursor = connection.cursor()
            cursor.execute("""  UPDATE seguidos SET dejado =? WHERE usuario=? AND seguidores = ?""",
                           ('Sorry', user, seg))
            connection.commit()
            connection.close()
            continue
        elif '<button class="BY3EC  sqdOP  L3NKy    _8A5w5    " type="button">Requested</button>' in source:
            connection = sqlite3.connect("Unfollowd.db")
            cursor = connection.cursor()
            cursor.execute("""  UPDATE seguidos SET dejado =? WHERE usuario=? AND seguidores = ?""",
                           ('requested', user, seg))
            connection.commit()
            connection.close()
            continue
        elif '<p>Please wait a few minutes before you try again.</p>' in source:
            print('se llego al limite')
            input('         ...')
            break
        else:
            if Solo_seg is False:
                followers = source.split(',"edge_followed_by":{"count":')[1]
                followers = followers.split('},"')[0]
                followers = followers.replace(".", "")
                followers = followers.replace(",", "")
                followers = int(followers.replace("k", "000"))

                following = source.split('</span> following</a></li></ul>')[0]
                following = following.split('<span class="g47SY ">')[-1]
                following = following.split('<')[0]
                following = following.replace(".", "")
                following = following.replace(",", "")
                following = int(following.replace("k", "000"))
            else:
                followers = 10
                following = 10

            # !!!!!!!!!!!!!!!!
            if usar_seguidores is False:
                seguidor.append(seg)
            unfollowd = False

            # se ovserva hace cuanto se agrego al usuario
            connection = sqlite3.connect("Unfollowd.db")
            cursor = connection.cursor()
            cursor.execute('SELECT rowid, *  FROM cuando_seguido WHERE usuario = ? AND seguidores = ? ', (user, seg))
            items = cursor.fetchall()
            if len(items) < 1:
                cursor.execute('INSERT INTO cuando_seguido VAlUES(?,?,?)', (user, seg, str(time.strftime("%d/%m/%Y"))))
                connection.commit()
            connection.close()
            items = items[0]
            fecha = items[3]
            fecha = fecha.split('/')

            fecha_a = str(time.strftime("%d/%m/%Y"))
            fecha_a = fecha_a.split('/')

            diferencia = (int(fecha_a[1]) - int(fecha[1])) * 30 + int(fecha_a[0]) - int(fecha[0])
            diferencia = abs(diferencia)

            print('followers: ', followers, '   following: ', following, '     lim min:  ', Lim_minutos,
                  '     lim dia:  ', Lim_diario, '        ', seg, )

            if Solo_seg is True:
                masde = followers - 1

            # si no sigue al usuario, o sigue a mas perfiles de los que lo siguen, o tiene mas de 1000 seguidores, lo deja de seguir
            if seg not in seguidor or (followers * dosres) < following or followers > masde and diferencia > dias:
                if check_exists_by_class('glyphsSpriteFriend_Follow',browser) is True:
                    time.sleep(3)
                    browser.find_element_by_class_name('glyphsSpriteFriend_Follow').click()
                    time.sleep(4)
                    if check_exists_by_class('-Cab_', browser) is True:
                        browser.find_element_by_class_name('-Cab_').click()
                    elif check_exists_by_class('aOOlW -Cab_   ', browser) is True:
                        browser.find_element_by_class_name('aOOlW -Cab_   ').click()
                    time.sleep(5)
                    unfollowd = True

                else:
                    print('no se encuentra el boton para dejar de seguir, salteado')


                if unfollowd is True:
                    # los perfiles dejados, quedan guardados para no volver a seguirlos
                    connection = sqlite3.connect("Unfollowd.db")
                    cursor = connection.cursor()
                    cursor.execute("""  UPDATE seguidos SET dejado =? WHERE usuario=? AND seguidores = ?""",
                                   ('unfollowed', user, seg))
                    connection.commit()
                    connection.close()

                    # control para no ir mas rapido de lo que instagram deja
                    Lim_minutos = Lim_minutos - 1
                    Lim_diario = Lim_diario - 1
                    if Lim_diario < 1:
                        return
                    if Lim_minutos < 1:
                        print('********************************************************************')
                        print('Inicio del descanso', str(time.strftime("%H:%M:%S")))
                        print('********************************************************************')
                        time.sleep(400)
                        Lim_minutos = limite_mediahora
                        print('Fin del descanso', str(time.strftime("%H:%M:%S")))
                        print('********************************************************************')
            else:
                # si no fue dejado, se lo guarda para no volver a pasar por este devuelta
                connection = sqlite3.connect("Unfollowd.db")
                cursor = connection.cursor()
                cursor.execute("""  UPDATE seguidos SET dejado =? WHERE usuario=? AND seguidores = ?""",
                               ('not-unfollowed', user, seg))
                connection.commit()
                connection.close()

        connection = sqlite3.connect("Unfollowd.db")
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM seguidos WHERE usuario= ? AND seguidores = ?", (user, seg))
        items = cursor.fetchall()

        # Todo el print para que entienda mejor el usuario
        if Solo_seg is True:
            if seg not in seguidor and diferencia > 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Dejado, No es seguidor')
                print('')
            else:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2], '   No fue dejado')
                print('')
        else:
            if seg not in seguidor and diferencia > 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Dejado, No es seguidor')
                print('')
            elif (followers * 1.3) < following and diferencia > 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Dejado, Muchos mas seguidos que seguidores')
                print('')
            elif followers > 1000 and diferencia > 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Dejado, Muchos seguidores')
                print('')
            elif (seg not in seguidor or (followers * 1.3) < following or followers > 10000) and diferencia < 7:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2],
                      '   Agregado recientenmente')
                print('')
            else:
                print(str(seguidos.index(seg)), ' de ', str(len(seguidos)), '%30s' % items[0][2], '   No fue dejado')
                print('')

    browser.close()

def check_exists_by_xpath(xpath, browser):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_class(clas, browser):
    try:
        browser.find_element_by_class_name(clas)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_name(clas, browser):
    try:
        browser.find_element_by_name(clas)
    except NoSuchElementException:
        return False
    return True

def insta_Foll(Perfiles, limite_diario, limite_mediahora, Espera, user, passw):
    print('perfiles: ', Perfiles)
    print('limite_diario: ', limite_diario)
    print('limite_mediahora: ', limite_mediahora)


    # habre una ventan de chrome, entra en instagram y se loguea
    browser = webdriver.Chrome('chromedriver', desired_capabilities={'nativeEvents': False, })
    url = "https://www.instagram.com/accounts/login/?source=auth_switcher"
    browser.get(url)
    time.sleep(4)
    username = browser.find_element_by_name("username")
    password = browser.find_element_by_name("password")
    username.send_keys(user)
    password.send_keys(passw)
    time.sleep(1)

    if check_exists_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button/div",browser) is True:
        browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button/div").click()
    else:
        browser.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[3]/button/div').click()


    time.sleep(5)
    # variables globales
    Lim_30_minutos = limite_mediahora
    Lim_diario = limite_diario

    # abre lista de personas que  dejado de seguir en el pasado
    connection = sqlite3.connect("Unfollowd.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM cuando_seguido WHERE usuario = ? ", (user,))
    items = cursor.fetchall()
    dontfollow = []
    for item in items:
        dontfollow.append(item[2])
    connection.close()
    # circula en perfiles donde agregar
    for perfil in Perfiles:
        # ir al perfil señalado
        browser.get('https://www.instagram.com/' + perfil + '/?hl=en')

        # lee la cantidad de followers
        source = browser.page_source
        aux_data = (source.replace(',', '')).split('</span> followers</a>')
        aux_data2 = str(aux_data[0]).split('">')
        if 'k' in aux_data2[-1]:
            string = str(aux_data2[-1])
            followers = float(string[0:-1]) * 1000
        else:
            followers = float(aux_data2[-1])

        # abrer la lista defollowers
        time.sleep(3)
        browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(5)

        # variables reseteables en cada perfil
        personas = []
        personas2 = []
        personas2 = []
        estado = []
        Per_Es = {}

        # da tiempo a cargar
        time.sleep(25)

        # ayuda a cargar
        path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[12]")
        if check_exists_by_xpath(path, browser) is True:
            element = browser.find_element_by_xpath(path);
            browser.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(2)

        # mira toda la lista de seguidores
        for i in range(1, int(followers - 10)):
            # scroll dentro de ventana de dialogo
            path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]")
            if check_exists_by_xpath(path, browser) is True:
                element = browser.find_element_by_xpath(path);
                browser.execute_script("arguments[0].scrollIntoView(true);", element);
            else:
                time.sleep(2)
                if check_exists_by_xpath(path, browser) is True:
                    element = browser.find_element_by_xpath(path);
                    browser.execute_script("arguments[0].scrollIntoView(true);", element);
                else:
                    print('break')
                    break
            time.sleep(0.1)

            # obtiene los nombres de los perfiles y si se pueden seguir
            source = browser.page_source
            elementos = source.split('wo9IH')
            elementos.pop(0)
            if 'uu6c_' not in elementos[-1]:
                elementos.pop(-1)
            for t in range(+len(Per_Es) - len(elementos), -1):
                personas.append(str(elementos[t]).split('><img alt="')[1])
                personas2.append(str(personas[-1]).split("\'s profile picture")[0])
                if 'profile picture" class' in personas2[-1]:
                    personas2.pop(-1)
                estado.append(str(elementos[t]).split('type="button">')[-1])
                # armar un diccionario con usuario y condicon
                Per_Es[str(personas2[-1])] = str(estado[-1]).split('</button>')[0]

            # si el usuario sigue al perfil corrije un diccionario
            if user in Per_Es:
                Per_Es[user] = 'Following'

            # chekea que no se cargue la lista y le da tiempo o pasa a otro perfil
            if len(personas2) < (i + 1):
                print('Instagram con lag, reiniciaando . . . ')
                browser.quit()
                return insta_Foll(Perfiles, Lim_diario, limite_mediahora, Espera, user, passw)

            if len(personas2) < (i + 2):
                time.sleep(30)
                path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i - 10) + "]")
                if check_exists_by_xpath(path, browser) is True:
                    element = browser.find_element_by_xpath(path);
                    browser.execute_script("arguments[0].scrollIntoView(true);", element);
                time.sleep(30)
                path = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]")
                if check_exists_by_xpath(path, browser) is True:
                    element = browser.find_element_by_xpath(path);
                    browser.execute_script("arguments[0].scrollIntoView(true);", element);
                time.sleep(5)

            if personas2[i - 1] in dontfollow:
                print('Viendo perfil numero: ', i, '%30s' % personas2[i - 1], ', Ya fue seguida en algun momento')
            else:
                print('Viendo perfil numero: ', i, '%30s' % personas2[i - 1], ',', Per_Es[personas2[i - 1]],
                      Lim_30_minutos, Lim_diario)

            # sigue a las personas que puede, que no alla dejado de seguir
            if Per_Es[personas2[i - 1]] == 'Follow' and personas2[i - 1] not in dontfollow:
                time.sleep(2)
                Lim_30_minutos = Lim_30_minutos - 1
                Lim_diario = Lim_diario - 1

                # clikea
                button = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]/div/div[2]/button")
                button2 = ("/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(i) + "]/div/div[3]/button")
                if check_exists_by_xpath(button, browser) is True:
                    browser.find_element_by_xpath(button).click()
                    time.sleep(random.randint(2, 3))
                elif check_exists_by_xpath(button2, browser) is True:
                    browser.find_element_by_xpath(button2).click()
                    time.sleep(random.randint(2, 3))
                else:
                    print('FALLO EL CLICK')

                # guarda la fecha cuando se agrego
                connection = sqlite3.connect("Unfollowd.db")
                cursor = connection.cursor()
                cursor.execute('INSERT INTO cuando_seguido VAlUES(?,?,?)',
                               (user, personas2[i - 1], str(time.strftime("%d/%m/%Y"))))
                connection.commit()

            # si termina un perfil lo guarda
            if i > int(followers - 15):
                conn = sqlite3.connect('menu.db')
                c = conn.cursor()
                c.execute("UPDATE lista_perfiles SET echo = 'listo' WHERE perfil =? AND usuario = ?", (perfil, user))
                conn.commit()
                conn.close()

            # chekea limite diario y horario
            if Lim_diario < 1:
                print('Limite diario')
                break
            if Lim_30_minutos < 1:
                print('********************************************************************')
                print('Inicio del descanso', str(time.strftime("%H:%M:%S")))
                print('********************************************************************')
                time.sleep(random.randint(Espera * 59, Espera * 69))
                Lim_30_minutos = limite_mediahora
                print('Fin del descanso', str(time.strftime("%H:%M:%S")))
                print('********************************************************************')
    browser.close()

def menu_prinsipal():
    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    print('********************************************************************')
    print('                   bienvenide -- Insta.Bot')
    print('********************************************************************')
    print('')

    print('                     seleccione usuarie:')
    Perfiles = []
    c.execute("SELECT * FROM Usuaries")
    Usuaries = c.fetchall()
    for items in Usuaries:
        print(int(Usuaries.index(items)) + 1, items[0], )
        print('')

    print('0.', 'Otre')

    entrada = 'k'
    while entrada not in '101112013141516171819':
        entrada = str(input('...   '))

    clear()
    if entrada == '0':
        Use = input('Usuarie...')
        Pas = input('Contraseña...')
        c.execute("INSERT INTO Usuaries VALUES(?,?,?)", (Use, Pas, str(time.strftime("%d/%m---%H:%M"))))
        conn.commit()
        Usuaries = c.fetchall()
        conn.close()
    elif entrada in '101112013141516171819':
        entrada = int(entrada)
        Use = Usuaries[entrada - 1][0]
        Pas = Usuaries[entrada - 1][1]
    clear()
    return menu_secundario(Use, Pas)

def eliminar_use(Use):
    print('********************************************************************')
    print('                   Eliminando... -- ' + str(Use))
    print('********************************************************************')


    entrada = '0'
    while entrada not in 'siSInoNO':
        entrada = input('Seguro BORRAR '+ str(Use) + ".... SI / NO ..?")

    if entrada in 'noNO':
        return menu_prinsipal()
    else:
        connection = sqlite3.connect('Unfollowd.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM seguidos WHERE usuario=?', (Use,))
        cursor.execute('DELETE FROM seguidor WHERE usuario=?', (Use,))
        cursor.execute('DELETE FROM cuando_seguido WHERE usuario=?', (Use,))
        connection.commit()
        connection.close()


        connection = sqlite3.connect('menu.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM lista_perfiles WHERE usuario=?', (Use,))
        cursor.execute('DELETE FROM Usuaries WHERE usuario=?', (Use,))
        connection.commit()
        connection.close()
        time.sleep(1)
        clear()
        return menu_prinsipal()

def agregar_perf(Use, Pas, config):
    print('********************************************************************')
    print('                   Perfiles a agregar -- ' + str(Use))
    print('********************************************************************')
    print('')
    print('')

    conn = sqlite3.connect('menu.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lista_perfiles WHERE usuario =:usuario", {'usuario': Use})
    perfiles_usuario = c.fetchall()
    conn.commit()
    conn.close()

    for items in range(0, len(perfiles_usuario)):
        print(perfiles_usuario[items][0], perfiles_usuario[items][2])
        print('')
    print('')
    print('1. Agregar perfiles a la lista')
    print('2. Eliminar perfiles a la lista')
    print('3. Iniciar, predeterminado')
    print('4. Iniciar, personalizado')
    print('5. Volver')

    entrada_1 = 'pop'
    while entrada_1 not in '12345':
        entrada_1 = str(input('....'))
    time.sleep(0.1)
    if entrada_1 == '1':
        print(
            'Agregue el nombre del perfil a agregar, de a uno a la vez, luego "Enter". Para terminar precione 0 + "Enter"')
        while entrada_1 != str(0):
            entrada_1 = input('...')
            if entrada_1 != str(0):
                connection = sqlite3.connect('menu.db')
                c = connection.cursor()
                c.execute("INSERT INTO lista_perfiles VALUES(?,?,?)", (entrada_1, Use, 'pendiente'))
                connection.commit()
                connection.close()
        clear()
        agregar_perf(Use, Pas, config)
    elif entrada_1 == '2':
        print(
            'Agregue el nombre del perfil a eliminar, de a uno a la vez, luego "Enter". Para terminar precione 0 + "Enter"')
        while entrada_1 != '0':
            entrada_1 = input('...')
            if entrada_1 != '0':
                connection = sqlite3.connect('menu.db')
                c = connection.cursor()
                c.execute('DELETE FROM lista_perfiles WHERE usuario=? AND perfil=?', (Use, entrada_1))
                connection.commit()
                connection.close()
        clear()
        agregar_perf(Use, Pas, config)
    elif entrada_1 == '3':

        connection = sqlite3.connect('menu.db')
        c = connection.cursor()
        c.execute("SELECT * FROM lista_perfiles WHERE usuario =? AND echo =?", (Use, 'pendiente',))
        perfiles = c.fetchall()
        connection.close()

        Perfiles = []
        for items in range(0, len(perfiles)):
            Perfiles.append(perfiles[items][0])
        clear()
        print('inicio....')

        return insta_Foll(Perfiles, config[2], config[3], 30, Use, Pas)

    elif entrada_1 == '4':

        dia = int(input('Limite diario ...'))
        min =  int(input('Limite cada 30 minutos ...'))
        connection = sqlite3.connect('menu.db')
        c = connection.cursor()
        c.execute("SELECT * FROM lista_perfiles WHERE usuario =? AND echo =?", (Use, 'pendiente',))
        perfiles = c.fetchall()
        connection.close()

        Perfiles = []
        for items in range(0, len(perfiles)):
            Perfiles.append(perfiles[items][0])
        clear()
        print('inicio....')

        return insta_Foll(Perfiles, dia ,min, 30, Use, Pas)


    elif entrada_1 == '5':
        clear()
        return menu_secundario(Use, Pas)

def eliminar_perf(Use, Pas, config):
    print('********************************************************************')
    print('                    Dejar de seguir con -- ' + str(Use))
    print('********************************************************************')
    print('')
    print('')

    print('1. Actualizar tablas')
    print('2. Eliminar un perfil de la tabla')
    print('3. Iniciar, predeterminado')
    print('4. Iniciar, personalizado')
    print('5. Volver')
    entrada = 'pop'
    while entrada not in '12345':
        entrada = str(input("..."))
    if entrada in '1':
        insta_Unfoll(config[4], config[5], True, True, Use, Pas,config[8],config[9],config[10],config[11])
    elif entrada in '2':
        print('')
        print('')
        print('escriba un perfil a eliminar de la lista + enter, para finalizar 0')
        print('')
        print('')
        entrada = 1
        while entrada != '0':
            entrada = str(input("eliminar..."))
            connection = sqlite3.connect("Unfollowd.db")
            cursor = connection.cursor()
            cursor.execute("""  UPDATE seguidos SET dejado =? WHERE usuario=? AND seguidores = ?""",
                           ('unfollowed', Use, entrada))
            connection.commit()
            connection.close()
        return eliminar_perf(Use, Pas, config)
    elif entrada == '3':
        clear()
        return insta_Unfoll(config[4], config[5], False, False, Use, Pas,config[8],config[9],config[10],config[11])
    elif entrada == '4':

        dia = int(input('Limite diario ...'))
        min = int(input('Limite cada 10 minutos ...'))
        clear()
        return insta_Unfoll(dia, min, False, False, Use, Pas,config[8],config[9],config[10],config[11])

    else:
        return menu_secundario(Use, Pas , config)

def configuracion(Use, Pas, config):
    print('limite, dia seguir', config[2])
    print('limite, 30 minutos seguir', config[3])
    print('limite, dia dejar de seguir', config[4])
    print('limite, 10 minutos dejar de seguir', config[5])
    print('Solo dejar de seguir no seguidores',config[8])
    print('Taza de seguidos/seguidores para dejar',config[9])
    print('Dejar de seguir a partir de x seguidos:',config[10])
    print('Esperar x dias antes de dejar de seguir', config[11])

    print('')
    print('1. Cambiar')
    print('2. Volver')
    print('3. Restablecer')

    entrada = '0'
    while entrada not in '123':
        entrada = input('...')

    connection = sqlite3.connect('menu.db')
    cursor = connection.cursor()

    if entrada in '1':
        entrada = int(input('limite, dia seguir'))
        cursor.execute("""	UPDATE ajustes SET lim_dia_foll = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('limite, 30 minutos seguir'))
        cursor.execute("""	UPDATE ajustes SET lim_hora_foll = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('limite, dia dejar de seguir'))
        cursor.execute("""	UPDATE ajustes SET lim_dia_unfoll = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('limite, 10 minutos dejar de seguir'))
        cursor.execute("""	UPDATE ajustes SET lim_hora_unfoll = ? WHERE usuario = ? """, (entrada, Use))

        entrada='pop'
        while entrada not in 'siSISinoNoNO':
            entrada = input('Solo dejar de seguir "no seguidores" (SI/NO)')
        cursor.execute("""	UPDATE ajustes2 SET Solo_seg = ? WHERE usuario = ? """, (entrada, Use))

        entrada = float(input('Taza de seguidos/seguidores para dejar'))
        cursor.execute("""	UPDATE ajustes2 SET dosres = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('Dejar de seguir a partir de x seguidos:'))
        cursor.execute("""	UPDATE ajustes2 SET mas_de_tantos = ? WHERE usuario = ? """, (entrada, Use))

        entrada = int(input('Esperar x dias antes de dejar de seguir'))
        cursor.execute("""	UPDATE ajustes2 SET dias = ? WHERE usuario = ? """, (entrada, Use))

        connection.commit()
        connection.close()

    elif entrada in '3':
        cursor.execute("""	UPDATE ajustes SET lim_dia_foll = ? WHERE usuario = ? """, (400, Use))

        cursor.execute("""	UPDATE ajustes SET lim_hora_foll = ? WHERE usuario = ? """, (30, Use))

        cursor.execute("""	UPDATE ajustes SET lim_dia_unfoll = ? WHERE usuario = ? """, (300, Use))

        cursor.execute("""	UPDATE ajustes SET lim_hora_unfoll = ? WHERE usuario = ? """, (10, Use))

        cursor.execute("""	UPDATE ajustes2 SET Solo_seg = ? WHERE usuario = ? """, ('NO', Use))

        cursor.execute("""	UPDATE ajustes2 SET dosres = ? WHERE usuario = ? """, (1.3, Use))

        cursor.execute("""	UPDATE ajustes2 SET mas_de_tantos = ? WHERE usuario = ? """, (1000, Use))

        cursor.execute("""	UPDATE ajustes2 SET dias = ? WHERE usuario = ? """, (7, Use))

        connection.commit()
        connection.close()
    clear()
    menu_secundario(Use, Pas)

def menu_secundario(Use, Pas):
    clear()
    connection = sqlite3.connect("menu.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM ajustes WHERE usuario = ?", (Use,))
    items = cursor.fetchall()

    if len(items) == 0:
        cursor.execute(
            "insert into ajustes (usuario, lim_dia_foll,lim_dia_unfoll,lim_hora_foll,lim_hora_unfoll) VALUES(?,?,?,?,?);",
            [Use, 400, 300, 30, 10 ])
        connection.commit()

    cursor.execute("SELECT rowid, * FROM ajustes2 WHERE usuario = ?", (Use,))
    items = cursor.fetchall()

    if len(items) == 0:
        cursor.execute(
            "insert into ajustes2 (usuario, Solo_seg,dosres,mas_de_tantos,dias) VALUES(?,?,?,?,?);",
            [Use, 'NO', 1.3, 1000, 7])
        connection.commit()

    connection = sqlite3.connect("menu.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM ajustes WHERE usuario = ?", (Use,))
    connection.commit()
    config1 = cursor.fetchall()

    connection = sqlite3.connect("menu.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM ajustes2 WHERE usuario = ?", (Use,))
    connection.commit()

    config2 =cursor.fetchall()
    connection.close()
    config = config1[0] + config2[0]

    print('********************************************************************')
    print('                   bienvenide -- ' + str(Use))
    print('********************************************************************')

    print('')
    print('')
    print('')
    print('v. volver atras')
    print('0. Eliminar usuarie')
    print('1. Agregar Perfiles')
    print('2. Dejar de seguir perfiles')
    print('3. Configuracion')
    print('4. Agregar/Eliminar')
    print('5. Cambiar Contraseña')

    entrada = 'POP'
    while entrada not in '0123453vV':
        entrada = str(input('....  '))
    clear()

    if entrada == str(0):
        eliminar_use(Use)
        clear()
        return menu_prinsipal()

    if entrada == str(1):
        clear()
        return agregar_perf(Use, Pas, config)

    if entrada == str(2):
        clear()
        return eliminar_perf(Use, Pas, config)

    if entrada == str(3):
        clear()
        return configuracion(Use, Pas, config)

    if entrada in 'vV':
        clear()
        return menu_prinsipal()

    if entrada == "4":
        clear()
        conn = sqlite3.connect('menu.db')
        c = conn.cursor()
        c.execute("SELECT * FROM lista_perfiles WHERE usuario =? AND echo =?", (Use, 'pendiente',))
        perfiles = c.fetchall()
        conn.close()
        Perfiles = []
        for items in range(0, len(perfiles)):
            Perfiles.append(perfiles[items][0])
        print('inicio....')
        insta_Foll(Perfiles, config[2], config[3], 30, Use, Pas)

        insta_Unfoll(config[4], config[5], False, False, Use, Pas,config[8],config[9],config[10],config[11])

    if entrada == '5':
        clear()
        conn = sqlite3.connect('menu.db')
        c = conn.cursor()

        print('********************************************************************')
        print('                   Cambiar contraseña -- ' + str(Use))
        print('********************************************************************')

        print('')
        Pas = input('Nueva contraseña...')

        c.execute("update Usuaries set contra = ? where usuario = ?", (Pas, Use))
        conn.commit()
        conn.close()
        return menu_secundario(Use, Pas)

bases_datos()
menu = menu_prinsipal()

