import requests, datetime
from flask import Flask, render_template, redirect, json, request, session, Markup, flash

app = Flask(__name__)
app.secret_key = '8bf9547569cd5a638931a8639cf9f86237931e92' 
@app.route('/')
@app.route('/home')
def main():
	return render_template('home.html')

def convert_to_ft(value,given_units):
	conversions = {
	"m":3.28,
	"in":(1.0/12.0),
	"mm":(1.0/304.8),
	"ft":1
	}
	new_val = value*conversions[given_units]
	return new_val

@app.route('/',methods=['GET','POST'])
def getRate():
	params={}
	conversion = 10.764

	frame_length = float(request.form["frame_length"])
	frame_width = float(request.form["frame_width"])
	wood_width = float(request.form["wood_width"])
	margin_width = float(request.form["margin_width"])
	
	cost_wood_m = float(request.form["cost_wood_per_m"])
	cost_hw_sqft = float(request.form["cost_hw_per_sqft"])
	cost_trans_sqft = float(request.form["trans_charge_per_sqft"])
	cost_labour_sqft = float(request.form["labour_charge_per_sqft"])
	
	frame_length_units = request.form['frame_length_units']
	frame_width_units = request.form['frame_width_units']
	wood_width_units = request.form['wood_width_units']
	margin_width_units = request.form['margin_width_units']

	frame_length = convert_to_ft(frame_length,frame_length_units)
	frame_width = convert_to_ft(frame_width,frame_width_units)
	wood_width = convert_to_ft(wood_width,wood_width_units)
	margin_width = convert_to_ft(margin_width,margin_width_units)

	### converting cost of wood per m to cost of wood per sqft ###

	wood_length = convert_to_ft(1,"m")
	wood_area = wood_width*wood_length
	cost_wood_sqft = cost_wood_m/wood_area

	### everything is in sqft ####
	frame_area = frame_length*frame_width
	wood_length = frame_length

	actual_width = (margin_width/2.0) + wood_width
	
	is_divisible = False
	diff = frame_width%actual_width
	new_frame_width = frame_width
	if( diff <= 1.0):
		is_divisible = True
	else:
		new_frame_width = frame_width - diff
	session['diff'] = diff
	params['diff'] = diff
	no_of_woods = frame_width/actual_width

	wood_area = wood_width * wood_length
	total_area_wood = no_of_woods * wood_area
	
	cost_wood = total_area_wood * cost_wood_sqft
	cost_hw = frame_area * cost_hw_sqft
	cost_labour = frame_area * cost_labour_sqft
	cost_trans = frame_area * cost_trans_sqft

	total_cost = cost_wood + cost_hw + cost_labour + cost_trans

	session['cost'] = total_cost
	params['cost']=total_cost
	
	return render_template('rate.html',params = params)



@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
	print e
	msg =' There was an error. go to <a href="/home">home</a> page'
	return render_template('error.html', error=msg)

if __name__ == "__main__":
    app.run(debug=True,port=10002,use_evalex=False)
    # app.run(debug=True,host='192.168.43.53',port=5007,use_evalex=False)