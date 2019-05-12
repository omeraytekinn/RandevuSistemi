from sqlalchemy import create_engine,Column, Integer, String ,ForeignKey,case,DateTime
from sqlalchemy.orm import column_property, relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine('sqlite:///Randevu.db',echo=True, connect_args={'check_same_thread':False})#interface of database
Base = declarative_base()
class User(Base):
   __tablename__ = 'user'
   id = Column(Integer, primary_key=True)
   username = Column(String(50))
   password= Column(String(50))
   name=Column(String(50))
   surname=Column(String(50))
   email=Column(String(50))
   number=Column(String(50))
   adres=Column(String(50))
   user_type=Column(String(50))#kullanıcı

   __mapper_args__ = {'polymorphic_on':user_type,'polymorphic_identity':"User"}
   def __repr__(self):
      return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)

class Student(User):
   __tablename__ = 'student'
   Stu_id = Column(Integer,ForeignKey('user.id'),primary_key=True)
   __mapper_args__={'polymorphic_identity':'Student'}

class Teacher(User):
   __tablename__ = 'teacher'
   Tea_id = Column(Integer,ForeignKey('user.id'),primary_key=True)
   __mapper_args__={'polymorphic_identity':'Teacher'}



class Randevu(Base):
   __tablename__='randevu'
   id=Column(Integer,primary_key=True)
   teacher_id=Column(Integer,ForeignKey('teacher.Tea_id'))
   student_id=Column(Integer,ForeignKey('student.Stu_id'))
   created_date = Column(DateTime, default=datetime.datetime.utcnow)
   statue=Column(String(50))
   randevu_type = column_property(
      case(
      [(statue == "DN", "GecmisRandevu"),(statue == "FT", "GelecekRandevu")],
      else_="Randevu")
      )
   __mapper_args__ = {'polymorphic_on':randevu_type,'polymorphic_identity':"Randevu"}



class GerceklesenRandevu(Randevu):
   __tablename__='gecmisrandevu'
   Gerceklesen_id=Column(Integer,ForeignKey('randevu.id'),primary_key=True)
   Pteacher_id=Column(Integer)
   Pstudent_id=Column(Integer)
   past_date = Column(DateTime)
   NoteOfStudent =Column(String(256))
   NoteOfTeacher=Column(String(256))
   __mapper_args__ ={'polymorphic_identity':"GecmisRandevu"}

class GelecekRandevu(Randevu):
   __tablename__='gelecekrandevu'
   Gelecek_id=Column(Integer,ForeignKey('randevu.id'),primary_key=True)
   Fteacher_id=Column(Integer)
   Fstudent_id=Column(Integer)
   future_date= Column(DateTime)
   NoteOfStudent = Column(String(256))
   __mapper_args__ ={'polymorphic_identity':"GelecekRandevu"}


class TalepRandevu(Randevu):
   __tablename__='taleprandevu'
   Talep_id=Column(Integer,ForeignKey('randevu.id'),primary_key=True)

   __mapper_args__ ={'polymorphic_identity':"TalepRandevu"}



def OgrenciEkle(ad,soyad,kullanici,sifre,adres,email,number):
   Session = sessionmaker(bind=engine)
   session = Session()
   stu=Student(username=kullanici,password=sifre,name=ad,surname=soyad,adres=adres,email=email,number=number)
   session.add(stu)
   session.commit()

def OgretmenEkle(ad,soyad,kullanici,sifre,adres,email,number):
   Session = sessionmaker(bind=engine)
   session = Session()
   tea=Teacher(username=kullanici,password=sifre,name=ad,surname=soyad,adres=adres,email=email,number=number)
   session.add(tea)
   session.commit()

def GetPassword(username):
   Session = sessionmaker(bind=engine)
   session = Session()
   password=session.query(User.password).filter(User.username==username).scalar()
   session.commit()
   return password

def DeleteUser(id):
   Session = sessionmaker(bind=engine)
   session = Session()
   usertype=session.query(User.user_type).filter(User.id==id).scalar()
   session.commit()

def GetId(username):
   Session = sessionmaker(bind=engine)
   session = Session()
   id=session.query(User.id).filter(User.username==username).scalar()
   session.commit()
   return id

def UpdateUser(id,user2):
   Session = sessionmaker(bind=engine)
   session = Session()
   user=session.query(User).filter(User.id==id).scalar()
   user.name=user2.name
   user.surname=user2.surname
   user.email=user2.email
   user.number=user2.number
   user.adres=user2.adres
   session.commit()

def GetUser(id):
   Session = sessionmaker(bind=engine)
   session = Session()
   user=session.query(User).filter(User.id==id).scalar()
   session.commit()
   return user

def GetTeachers():
   Session = sessionmaker(bind=engine)
   session = Session()
   teachers=session.query(Teacher).all()
   session.commit()
   return teachers

#OgretmenEkle('ziya','kaba','ziyas','asde3241','yeldiz sok.','ziya@gmail.com','533432123')
   
#Base.metadata.create_all(engine)
#OgrenciEkle('alperen','aksu','aaksu','1234','mefkure sok.','aksulperen@gmail.com','535532123')
#Session = sessionmaker(bind=engine)
#session = Session()
#session.query(Student).filter(Student.Stu_name=='alperen').delete()
#session.commit()
#pass1=GetPassword('as')
#print (pass1)
