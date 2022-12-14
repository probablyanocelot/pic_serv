from dataclasses import dataclass
from producer import publish

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_serialize import FlaskSerialize
# from flask_restful import Resource, reqparse
# import werkzeug

from sqlalchemy import UniqueConstraint

from config import postgres_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_uri
CORS(app)

db = SQLAlchemy(app)
fs_mixin = FlaskSerialize(db)


@dataclass
class Image(db.Model, fs_mixin):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    datetime_taken = db.Column(db.String(200), nullable=True)
    # meta_data =


@ app.route('/api/images')
@ app.route('/api/image/<int:image_id>')
def index(image_id=None):
    # data = Image.query.all()
    # result = [d.__dict__ for d in data]
    # return jsonify(result=result)
    # return jsonify(Image.query.all())
    return Image.fs_get_delete_put_post(image_id)


@ app.route('/api/images/add', methods=['POST'])  # <int:id>/add
def add_picture(added_image):
    try:
        image = Image(title=added_image.name, format=added_image.format)
        db.session.add(image)
        db.session.commit()

        publish('picture_received', id)

    except:
        abort(400, "You already liked this product")

    return jsonify({
        'message': 'success',
    })


def upload_image():
    parse = reqparse.RequestParser()
    parse.add_argument(
        'file', type=werkzeug.datastructures.FileStorage, location='files')
    args = parse.parse_args()
    image_file = args['file']
    image_file.save("your_file_name.jpg")

# @dataclass
# class ProductUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     product_id = db.Column(db.Integer)

#     UniqueConstraint('user_id', 'product_id', name='user_product_unique')


# @app.route('/api/products/<int:id>/like')
# def like(id):
#     req = requests.get('http://docker.for.mac.localhost:8000/api/user')
#     json = req.json()

#     try:
#         productUser = ProductUser(user_id=json['id'], product_id=id)
#         db.session.add(productUser)
#         db.session.commit()

#         publish('product_liked', id)

#     except:
#         abort(400, "You already liked this product")

#     return jsonify({
#         'message': 'success',
#     })
db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7777)
