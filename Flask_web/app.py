from flask import Flask, render_template, request, flash, redirect, url_for
from model import db, house_data_cleaning, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "It's a secret. I'm not telling you!!! "
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{'root'}:{'123456'}@{'localhost'}:{3306}/{'pydb'}"

db.init_app(app)

@app.route('/')#索引
def index():
    return redirect(url_for('login'))

@app.route('/login', methods = ['POST', 'GET'])#登录
def login():
    if request.method == "POST":
        account = request.form['account']
        password = request.form['password']
        user = User.query.filter_by(account=account).first()
        if user and user.password == password:
            flash('登录成功！', 'success')
            return redirect(url_for('menu'))
        else:
            flash('登录失败，请检查账户或密码是否正确！', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])#注册
def register():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        if User.query.filter_by(account=account).first():
            flash('注册失败，该账户已存在！', 'error')
            return redirect(url_for('register'))
        new_user = User(account=account, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功，点击返回登录！')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/menu')#主页
def menu():
    return render_template("menu.html")

@app.route('/region_sum', methods=['GET'])
def region_sum():
    get_all =  house_data_cleaning.query.all()
    regions = [h.house_Region for h in get_all]
    return render_template("region_sum.html", regions = regions)

@app.route('/region_average_price', methods=['GET'])
def region_average_price():
    get_all = house_data_cleaning.query.all()
    regions = [h.house_Region for h in get_all]
    prices = [h.house_Price for h in get_all]
    return render_template("region_average_price.html", regions = regions, prices = prices)

@app.route('/region_price')
def region_price():
    get_all = house_data_cleaning.query.all()
    regions = [h.house_Region for h in get_all]
    prices = [h.house_Price for h in get_all]
    return render_template("region_price.html", regions = regions, prices = prices)

@app.route('/type_sum')
def type_sum():
    get_all = house_data_cleaning.query.all()
    types = [h.house_Type for h in get_all]
    return render_template("type_sum.html", types = types)

@app.route('/area_sum')
def area_sum():
    get_all = house_data_cleaning.query.all()
    areas = [h.house_Area for h in get_all]
    return render_template("area_sum.html", areas = areas)

@app.route('/price_sum')
def price_sum():
    get_all = house_data_cleaning.query.all()
    prices = [h.house_Price for h in get_all]
    return render_template("price_sum.html", prices = prices)

@app.route('/area_price')
def area_price():
    get_all = house_data_cleaning.query.all()
    prices = [h.house_Price for h in get_all]
    areas = [h.house_Area for h in get_all]
    return render_template("area_price.html", prices=prices, areas = areas)

@app.route('/region_price02')
def region_price02():
    get_all = house_data_cleaning.query.all()
    regions = [h.house_Region for h in get_all]
    prices = [h.house_Price for h in get_all]
    return render_template("region_price02.html", regions=regions, prices=prices)

@app.route('/region_price_area')
def region_price_area():
    get_all = house_data_cleaning.query.all()
    regions = [h.house_Region for h in get_all]
    prices = [h.house_Price for h in get_all]
    areas = [h.house_Area for h in get_all]
    return render_template("region_price_area.html", regions=regions, prices=prices, areas = areas)

@app.route('/house_all')
def house_all():
    get_all = house_data_cleaning.query.all()
    introduce = [h.house_Introduce for h in get_all]
    region = [h.house_Region for h in get_all]
    address = [h.house_Address for h in get_all]
    types = [h.house_Type for h in get_all]
    area = [h.house_Area for h in get_all]
    floor = [h.house_floor for h in get_all]
    direction = [h.house_Direction for h in get_all]
    price = [h.house_Price for h in get_all]
    heating = [h.house_Heating for h in get_all]
    lease = [h.house_Lease for h in get_all]
    house = []
    for i in range(len(introduce)):
        house.append([introduce[i], region[i], address[i], types[i], area[i], floor[i], direction[i], price[i], heating[i], lease[i]])
    return render_template("house_all.html", houses = house)

if __name__ == '__main__':
    app.run(tdebug = True)
