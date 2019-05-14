from sqlalchemy import create_engine,Column, Integer, String ,ForeignKey,case,DateTime,Boolean
from sqlalchemy.orm import column_property, relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from flask import jsonify

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
      return self

class Student(User):
   __tablename__ = 'student'
   Stu_id = Column(Integer,ForeignKey('user.id',ondelete='CASCADE'),primary_key=True)
   __mapper_args__={'polymorphic_identity':'Student'}

class Teacher(User):
   __tablename__ = 'teacher'
   Tea_id = Column(Integer,ForeignKey('user.id',ondelete='CASCADE'),primary_key=True)
   note=Column(String(50))
   arastirma=Column(String(50))
   takvim=Column(String(50))
   __mapper_args__={'polymorphic_identity':'Teacher'}



class Randevu(Base):
   __tablename__='randevu'
   id=Column(Integer,primary_key=True)
   Topic=Column(String(50))
   teacher_id=Column(Integer,ForeignKey('teacher.Tea_id'))
   teacherName=Column(String,ForeignKey('user.name'))
   student_id=Column(Integer,ForeignKey('student.Stu_id'))
   teacherName=Column(String,ForeignKey('user.surname'))
   studentName=Column(String)
   Randevu_date=Column(DateTime)
   created_date = Column(DateTime, default=datetime.datetime.utcnow)
   randevu_type = Column(String(50))
   __mapper_args__ = {'polymorphic_on':randevu_type,'polymorphic_identity':"Randevu"}

class TalepRandevu(Randevu):
   __tablename__='taleprandevu'
   Talep_id=Column(Integer,ForeignKey('randevu.id'),primary_key=True)
   TalepNotu = Column(String(256))

   __mapper_args__ ={'polymorphic_identity':"TalepRandevu"}


class GelecekRandevu(Randevu):
   __tablename__='gelecekrandevu'
   Gelecek_id=Column(Integer,ForeignKey('randevu.id'),primary_key=True)
   OgretmenNotu = Column(String(256))#ogrencinin randevu talebine karşılık öğretmen tarafından cevap
   NoteOfStudent = Column(String(256))#ogrencinin talep notunun aynısı
   IsItPast = Column(Boolean,default=False)
   __mapper_args__ ={'polymorphic_identity':"GelecekRandevu"}

class GecmisRandevu(Randevu):
   __tablename__='gecmisrandevu'
   Gecmis_id=Column(Integer,ForeignKey('randevu.id'),primary_key=True)
   RanDegerNotu = Column(String(256))#Randevu Sonrası Öğretmen tarafından Oluşturulan Değerlendirme Yazısı
   __mapper_args__ ={'polymorphic_identity':"GecmisRandevu"}

def OgrenciEkle(ad,soyad,kullanici,sifre,adres,email,number):
   Session = sessionmaker(bind=engine)
   session = Session()
   stu=Student(username=kullanici,password=sifre,name=ad,surname=soyad,adres=adres,email=email,number=number)
   session.add(stu)
   session.commit()

def OgretmenEkle(ad,soyad,kullanici,sifre,adres,email,number,note):
   Session = sessionmaker(bind=engine)
   session = Session()
   tea=Teacher(username=kullanici,password=sifre,name=ad,surname=soyad,adres=adres,email=email,number=number,note=note)
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
   users = session.query(Student).filter(User.id ==id).all()
   users2 = session.query(Teacher).filter(User.id ==id).all()
   for user in users:
      session.delete(user)
   for user in users2:
      session.delete(user)
   session.commit()


def DeleteRandevu(id):
   Session = sessionmaker(bind=engine)
   session = Session()
   randevus = session.query(GecmisRandevu).filter(Randevu.id ==id).all()
   for randevu in randevus:
      session.delete(randevu)
   session.commit()
   Session = sessionmaker(bind=engine)
   session = Session()
   randevus2 = session.query(GelecekRandevu).filter(Randevu.id ==id).all()
   for randevu in randevus2:
      session.delete(randevu)
   session.commit()
   Session = sessionmaker(bind=engine)
   session = Session()
   randevus3 = session.query(TalepRandevu).filter(Randevu.id ==id).all()
   for randevu in randevus3:
      session.delete(randevu)
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

def UpdateTeacher(id,teacher2):
   Session = sessionmaker(bind=engine)
   session = Session()
   teacher=session.query(Teacher).filter(Teacher.Tea_id==id).scalar()
   teacher.name=teacher2.name
   teacher.surname=teacher2.surname
   teacher.email=teacher2.email
   teacher.number=teacher2.number
   teacher.adres=teacher2.adres
   teacher.note=teacher2.note2
   teacher.takvim=teacher2.takvim
   teacher.arastirma=teacher2.arastirma
   session.commit()

def GetUser(id):
   Session = sessionmaker(bind=engine)
   session = Session()
   user=session.query(User).filter(User.id==id).scalar()
   session.expunge_all()
   session.commit()
   return user

def GetTeacher(id):
  Session = sessionmaker(bind=engine)
  session = Session()
  teacher=session.query(Teacher).filter(Teacher.Tea_id==id).scalar()
  session.expunge_all()
  session.commit()
  return teacher

def GetTeachers():
   Session = sessionmaker(bind=engine)
   session = Session()
   teachers=session.query(Teacher).all()
   session.expunge_all()
   session.commit()
   return teachers


def GetGecmisRandevu(id):
   Session = sessionmaker(bind=engine)
   session = Session()
   randevus=session.query(GecmisRandevu).filter(GecmisRandevu.student_id==id).all()
   session.expunge_all()
   session.commit()
   return randevus


def GetGelecekRandevu(id):
   Session = sessionmaker(bind=engine)
   session = Session()
   randevus=session.query(GelecekRandevu).filter(GelecekRandevu.student_id==id).all()
   session.expunge_all()
   session.commit()
   return randevus

def GetTalepRandevu(id):
   Session = sessionmaker(bind=engine)
   session = Session()
   randevus=session.query(TalepRandevu).filter(TalepRandevu.student_id==id).all()
   session.expunge_all()
   session.commit()
   return randevus

def CheckDateTime():
   Session = sessionmaker(bind=engine)
   session = Session()
   randevus=session.query(GelecekRandevu).all()
   x = datetime.datetime.now()
   currenttime=datetime.datetime(x.year,x.month,x.day,x.hour,x.minute,x.second)
   for randevu in randevus:
      if randevu.Randevu_date < currenttime:
         randevu.IsItPast=True
   session.commit()



def RandevuOnay(id):
   Session = sessionmaker(bind=engine)
   session = Session()
   randevu=session.query(TalepRandevu).filter(TalepRandevu.Talep_id==id).scalar()
   id=randevu.Talep_id
   GelRandevu=GelecekRandevu(id=randevu.Talep_id,Topic=randevu.Topic,teacher_id=randevu.teacher_id,student_id=randevu.student_id,teacherName=randevu.teacherName,studentName=randevu.studentName,Randevu_date=randevu.Randevu_date,NoteOfStudent=randevu.TalepNotu)
   session.commit()
   DeleteRandevu(id)
   Session = sessionmaker(bind=engine)
   session = Session()
   session.add(GelRandevu)
   session.commit()

def RandevuBitir(id,RandevuNotu):
   Session = sessionmaker(bind=engine)
   session = Session()
   randevu=session.query(GelecekRandevu).filter(GelecekRandevu.Gelecek_id==id).scalar()
   id=randevu.Gelecek_id
   GecRandevu=GecmisRandevu(id=randevu.Gelecek_id,Topic=randevu.Topic,teacher_id=randevu.teacher_id,student_id=randevu.student_id,teacherName=randevu.teacherName,studentName=randevu.studentName,Randevu_date=randevu.Randevu_date,RanDegerNotu=RandevuNotu)
   session.commit()
   DeleteRandevu(id)
   Session = sessionmaker(bind=engine)
   session = Session()
   session.add(GecRandevu)
   session.commit()


def TalepOlustur(konu,teacher_id,student_id,teacherName,studentName,time):
   Session=sessionmaker(bind=engine)
   session=Session()
   randevu=TalepRandevu(Topic=konu,teacher_id=teacher_id,student_id=student_id,teacherName=teacherName,studentName=studentName,Randevu_date=time)
   session.add(randevu)
   session.commit()


#RandevuBitir(1,"asdasda")
#DeleteUser(3)
#DeleteRandevu(1)

#OgretmenEkle('ziya','kaba','ziyas','asde3241','yeldiz sok.','ziya@gmail.com','533432123')

#Base.metadata.create_all(engine)
#OgrenciEkle('alperen','aksu','alperen','1234','mefkure sok.','aksulperen@gmail.com','535532123')
#OgrenciEkle('ömer','aytekin','ömer','1234','mefkure sok.','aksulperen@gmail.com','535532123')
#OgrenciEkle('ufuk','yılmaz','ufuk','1234','mefkure sok.','aksulperen@gmail.com','535532123')
#OgretmenEkle('zeynep','akca','zeynep','1234','mefkure sok.','aksulperen@gmail.com','535532123',"asdasdasder")
#OgretmenEkle('amac','güven','amac','1234','mefkure sok.','aksulperen@gmail.com','535532123')
#OgretmenEkle('göksel','biricil','göksel','1234','mefkure sok.','aksulperen@gmail.com','535532123')
#Session = sessionmaker(bind=engine)
#session = Session()
#session.query(Student).filter(Student.Stu_name=='alperen').delete()
#rande=Randevu()
#session.add(rande)
#session.commit()
#pass1=GetPassword('as')
#print (pass1)
#time=datetime.datetime(2018,11,2)
#rand=TalepRandevu(Topic='konu',teacher_id=5,student_id=1,teacherName='amac',studentName='alperen',Randevu_date=time)
#rand2=GelecekRandevu(Topic='konu2',teacher_id=4,student_id=1,teacherName='cihan',studentName='alperen',Randevu_date=time)
#rand3=GecmisRandevu(Topic='konu3',teacher_id=4,student_id=1,teacherName='cihan',studentName='alperen',Randevu_date=time)
#Session = sessionmaker(bind=engine)
#session = Session()
#session.add(rand)
#session.add(rand2)
#session.add(rand3)
#session.commit()
