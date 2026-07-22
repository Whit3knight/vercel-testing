from flask import Flask, render_template
from flask import request, redirect, url_for
from mysql import connector
import os

app = Flask(__name__)

db = connector.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    user=os.environ.get('DB_USER', 'root'),
    passwd=os.environ.get('DB_PASS', ''),
    database=os.environ.get('DB_NAME', 'db_kuliah')
)

if db.is_connected():
    print(" KONEKSI KE DATABASE BERHASIL! ")

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM mahasiswa')
    result = cursor.fetchall()
    cursor.close()
    return render_template('index.html', hasil=result)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')


@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']

    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO mahasiswa (nim, nama, asal) VALUES (%s, %s, %s)',
        (nim, nama, asal)
    )
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/ubah/<nim>', methods=['GET'])
def ubah_data(nim):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM mahasiswa WHERE nim=%s', (nim,))
    result = cursor.fetchall()
    cursor.close()
    return render_template('ubah.html', hasil=result)


@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    nim_ori = request.form['nim_ori']
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']

    cursor = db.cursor()
    sql = "UPDATE mahasiswa SET nim=%s, nama=%s, asal=%s WHERE nim=%s"
    cursor.execute(sql, (nim, nama, asal, nim_ori))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/hapus/<nim>', methods=['GET'])
def hapus_data(nim):
    cursor = db.cursor()
    cursor.execute('DELETE FROM mahasiswa WHERE nim=%s', (nim,))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)