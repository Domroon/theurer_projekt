from flask import current_app, g


def test():
    with current_app.app_context():
        #test code
        admin = current_app.User(username='admin', email='admin@example.com')
        guest = current_app.User(username='guest', email='guest@example.com')

        g.db.session.add(admin)
        g.db.session.add(guest)
        g.db.session.commit()

        print(current_app.User.query.all())
        print(current_app.User.query.filter_by(username='admin').first())


def main():
    test()


if __name__ == '__main__':
    main()