from flask_website import app

def main():
    # try:
    #     print(sys.argv[1])
    #     if sys.argv[1] == 'init-db':
    #         db.drop_all()
    #         db.create_all()
    #         print(" * Database initialized")
    # except IndexError:
    #     pass

    app.run(debug=True)


if __name__ == '__main__':
    main()