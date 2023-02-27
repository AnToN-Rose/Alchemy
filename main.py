from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User (Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = relationship('Address', backref='user', uselist=False)
    contact = relationship("Contacts")


    def __repr__(self):
        return f" {self.id, self.name}"


class Address (Base):
    __tablename__ ='address'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    address = Column(String(100), nullable=False)

    def __repr__(self):
        return f" {self.address}"


class Contacts (Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    phone_number = Column(String(15), nullable=False)

    def __repr__(self):
        return f" {self.phone_number}"


engine = create_engine("sqlite:///user.db", echo = False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


new_users = [
        User(name='Bakhromjon'),
        User(name='Jamshid'),
        User(name='Ruslan')
    ]

session.add_all(new_users)
session.commit()

new_addresses = [
    Address(address='Chiltogon 10', user_id=new_users[0].id),
    Address(address='Qoraqamish', user_id=new_users[1].id),
    Address(address='Yunusobod',  user_id=new_users[2].id)
]
session.add_all(new_addresses)
# session.commit()

new_contacts = [
    Contacts(phone_number='998909894144', user_id=new_users[0].id),
    Contacts(phone_number='998911919012', user_id=new_users[1].id),
    Contacts(phone_number='998970034818', user_id=new_users[2].id)
]

session.add_all(new_contacts)


def add():
    print("Enter name, address and phone number")
    name = input('Name:')
    address = input('Address:')

    new_user = User(name=name)
    session.add(new_user)
    session.commit()
    new_address = Address(address=address, user_id=new_user.id)
    session.add(new_address)
    number_of_phones = int(input("How many numbers user have:"))
    for contact in range(0, number_of_phones):
        contact = input('Phone number:')
        new_contact = Contacts(phone_number=contact, user_id=new_user.id)
        session.add(new_contact)


add()
session.commit()
print(session.query(User).all())
print(session.query(User).filter(User.id == 1).all())
print(session.query(Address).filter(Address.user_id == 1).all())
print(session.query(Contacts).filter(Contacts.user_id == 1).all())
print(session.query(User, Address, Contacts).filter(User.id == 1).filter(Address.user_id == 1).filter(Contacts.user_id == 1).all())













