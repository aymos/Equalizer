#!usr/bin/env python

import pyaudio , kivy , struct , wave , os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.graphics import *
from kivy.uix.stacklayout import StackLayout
from kivy.core.audio import SoundLoader
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from functools import partial
from kivy.uix.filechooser import FileChooserListView

class WaveApp(Popup):

	def __init__(self, **kwargs):
		super(WaveApp, self).__init__(**kwargs)
		self.display()
		self.inputWaveFile1 = ''
		self.inputWaveFile2 = ''
		self.inputWaveFile3 = ''
		self.rec = []
		self.play1 = 0
		self.play2 = 0
		self.play3 = 0

	def display(self):

		layout1 = BoxLayout(orientation ='vertical')
		Heading = Label(text = '[b] Wave Mixer [/b]', font_size = 25, markup = True, size_hint = (1,0.1))
		layout1.add_widget(Heading)
		
		layout3 = BoxLayout(orientation = 'horizontal')
		
		layout2 = StackLayout(orientation = 'tb-lr')
		Title1 = Label(text = '[b]Wave 1[/b]', font_size = 20,size_hint = (1, 0.1) , color = (0,0.5,0.5,0),markup=True)
		selectFile1 = Button(text = 'Select File', size_hint = (1, 0.05))

		selectFile1.bind(on_press = self.selectSound1)
		
		Amplitude = Label(text = 'Amplitude', size_hint = (1, 0.1), markup = True,valign = 'middle', halign = 'center')
		self.slide1 = Slider(min = 1, max = 5, value = 1, size_hint = (0.9, 0.05))
		timeShift = Label(text = 'Time Shift', size_hint = (1, 0.1), markup = True, valign = 'middle', halign = 'center')
		self.slide2 = Slider(min = -16000, max = 16000, value = 0, size_hint = (0.9, 0.05))
		timeScale = Label(text = 'Time Scaling', size_hint = (1, 0.1), markup = True, valign = 'middle', halign = 'center',)
		self.slide3 = Slider(min = 0, max = 70, value = 35, size_hint = (0.9, 0.05))
		
		self.tReverse1 = 0
		self.Modulate1 = 0
		self.Mix1 = 0		
				
		timeReverse = Label(text = 'Time Reversal', size_hint = (0.85, 0.05), markup = True, halign = 'center', valign = 'middle')
		self.check1 = CheckBox(size_hint = (1, 0.06))
		Modulation = Label(text = 'Select For Modulation', size_hint = (0.85, 0.05), markup = True, halign = 'center', valign = 'middle')
		self.check2 = CheckBox(size_hint = (1, 0.06))
		Mixing = Label(text = 'Select For Mixing', size_hint = (0.85, 0.05), markup = True, halign = 'center', valign = 'middle')
		self.check3 = CheckBox(size_hint = (1, 0.06))
		PlayFile1 = Button(text ='PLAY / PAUSE', size_hint = (1, 0.05))
		
		PlayFile1.bind(on_press = self.playSound1)
		self.check1.bind(active = self.on_checkbox_active1)
		self.check2.bind(active = self.on_checkbox_active2)
		self.check3.bind(active = self.on_checkbox_active3)
		self.slide1.bind(value = self.ampScale1)
		self.slide2.bind(value = self.tShift1)
		self.slide3.bind(value = self.tScale1)

		layout2.add_widget(Title1)
		layout2.add_widget(selectFile1)
		layout2.add_widget(Amplitude)
		layout2.add_widget(self.slide1)
		layout2.add_widget(timeShift)
		layout2.add_widget(self.slide2)
		layout2.add_widget(timeScale)
		layout2.add_widget(self.slide3)
		layout2.add_widget(self.check1)
		layout2.add_widget(timeReverse)
		layout2.add_widget(self.check2)
		layout2.add_widget(Modulation)
		layout2.add_widget(self.check3)
		layout2.add_widget(Mixing)
		layout2.add_widget(PlayFile1)
		
		layout3.add_widget(layout2)
		
		layout2 = StackLayout(orientation = 'tb-lr')
		Title2 = Label(text = '[b]Wave 2[/b]', font_size = 20,size_hint = (1, 0.1) , color = (0,0.5,0.5,0),markup=True)
		selectFile2 = Button(text = 'Select File', size_hint = (1, 0.05))

		selectFile2.bind(on_press = self.selectSound2)
		Amplitude = Label(text = 'Amplitude', size_hint = (1, 0.1), markup = True,valign = 'middle', halign = 'center')
		self.slide4 = Slider(min = 1, max = 5, value = 1, size_hint = (0.9, 0.05))
		timeShift = Label(text = 'Time Shift', size_hint = (1, 0.1), markup = True, valign = 'middle', halign = 'center')
		self.slide5 = Slider(min = -16000, max = 16000, value = 0, size_hint = (0.9, 0.05))
		timeScale = Label(text = 'Time Scale', size_hint = (1, 0.1), markup = True, valign = 'middle', halign = 'center')
		self.slide6 = Slider(min = 0, max = 70, value = 35, size_hint = (0.9, 0.05))

		self.tReverse2 = 0
		self.Modulate2 = 0
		self.Mix2 = 0

		timeReverse = Label(text = 'Time Reversal', size_hint = (0.85, 0.05), markup = True, halign = 'center', valign = 'middle')
		self.check4 = CheckBox(size_hint = (1, 0.06))
		Modulation = Label(text = 'Select For Modulation', size_hint = (0.85, 0.05), markup = True, halign = 'center', valign = 'middle')
		self.check5 = CheckBox(size_hint = (1, 0.06))
		Mixing = Label(text = 'Select For Mixing', size_hint = (0.85, 0.05), markup = True, halign = 'center', valign = 'middle')
		self.check6 = CheckBox(size_hint = (1, 0.06))
		PlayFile2 = Button(text = 'PLAY / PAUSE', size_hint = (1, 0.05))

		PlayFile2.bind(on_press = self.playSound2)
		self.check4.bind(active = self.on_checkbox_active4)
		self.check5.bind(active = self.on_checkbox_active5)
		self.check6.bind(active = self.on_checkbox_active6)
		self.slide4.bind(value = self.ampScale2)
		self.slide5.bind(value = self.tShift2)
		self.slide6.bind(value = self.tScale2)
		
		layout2.add_widget(Title2)
		layout2.add_widget(selectFile2)
		layout2.add_widget(Amplitude)
		layout2.add_widget(self.slide4)
		layout2.add_widget(timeShift)
		layout2.add_widget(self.slide5)
		layout2.add_widget(timeScale)
		layout2.add_widget(self.slide6)
		layout2.add_widget(self.check4)
		layout2.add_widget(timeReverse)
		layout2.add_widget(self.check5)
		layout2.add_widget(Modulation)
		layout2.add_widget(self.check6)
		layout2.add_widget(Mixing)
		layout2.add_widget(PlayFile2)
		layout3.add_widget(layout2)
		
		layout2 = StackLayout(orientation = 'tb-lr')
		Title3 = Label(text = '[b]Wave 3[/b]', font_size = 20,size_hint = (1, 0.1) , color = (0,0.5,0.5,0),markup=True)
		selectFile3 = Button(text = 'Select File', size_hint = (1, 0.05))

		selectFile3.bind(on_press = self.selectSound3)
		
		Amplitude = Label(text = 'Amplitude', size_hint = (1, 0.1), markup = True,valign = 'middle', halign = 'center')
		self.slide7 = Slider(min = 1, max = 5, value = 1, size_hint = (0.9, 0.05))
		timeShift = Label(text = 'Time Shift', size_hint = (1, 0.1), markup = True, valign = 'middle', halign = 'center')
		self.slide8 = Slider(min = -16000, max = 16000, value = 0, size_hint = (0.9, 0.05))
		timeScale = Label(text = 'Time Scale', size_hint = (1, 0.1), markup = True, valign = 'middle', halign = 'center')
		self.slide9 = Slider(min = 0, max = 70, value = 35, size_hint = (0.9, 0.05))

		self.tReverse3 = 0
		self.Modulate3 = 0
		self.Mix3 = 0
		
		timeReverse = Label(text = 'Time Reversal', size_hint = (0.85, 0.05), markup = True, halign = 'center', valign = 'middle')
		self.check7 = CheckBox(size_hint = (1, 0.06))
		Modulation = Label(text = 'Select For Modulation', size_hint = (0.85, 0.05), markup = True, halign = 'center', valign = 'middle')
		self.check8 = CheckBox(size_hint = (1, 0.06))
		Mixing = Label(text = 'Select For Mixing', size_hint = (0.85, 0.05), markup = True, halign = 'center', valign = 'middle')
		self.check9 = CheckBox(size_hint = (1, 0.06))
		PlayFile3 = Button(text = 'PLAY / PAUSE', size_hint = (1, 0.05))
		
		PlayFile3.bind(on_press = self.playSound3)
		self.check7.bind(active = self.on_checkbox_active7)
		self.check8.bind(active = self.on_checkbox_active8)
		self.check9.bind(active = self.on_checkbox_active9)
		self.slide7.bind(value = self.ampScale3)
		self.slide8.bind(value = self.tShift3)
		self.slide9.bind(value = self.tScale3)

		layout2.add_widget(Title3)
		layout2.add_widget(selectFile3)
		layout2.add_widget(Amplitude)
		layout2.add_widget(self.slide7)
		layout2.add_widget(timeShift)
		layout2.add_widget(self.slide8)
		layout2.add_widget(timeScale)
		layout2.add_widget(self.slide9)
		layout2.add_widget(self.check7)
		layout2.add_widget(timeReverse)
		layout2.add_widget(self.check8)
		layout2.add_widget(Modulation)
		layout2.add_widget(self.check9)
		layout2.add_widget(Mixing)
		layout2.add_widget(PlayFile3)

		layout3.add_widget(layout2)
		layout1.add_widget(layout3)
		
		MixButt = Button(text = ' Mix and Play ', background_color = (0 , 0, 0.5, 0.8), size_hint = (1, 0.07),font_size=14)
		ModulateButt = Button(text = ' Modulate and Play ', background_color = (0 , 0.5, 0, 0.8), size_hint = (1, 0.07),font_size=14)
		RecordButt = Button(text='Record Audio',background_color=(0.5,0,0,0.8),size_hint=(1,.07),font_size=14)
		MixButt.bind(on_press = self.Mix)
		ModulateButt.bind(on_press = self.Modulate)
		RecordButt.bind(on_press = self.Record)		
		
		layout1.add_widget(MixButt)
		layout1.add_widget(ModulateButt)
		layout1.add_widget(RecordButt)
		self.add_widget(layout1)

	def Record(self, instance):
		chunk = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 44100
		RECORD_SECONDS = 5
		sound = pyaudio.PyAudio()
		stream = sound.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = chunk)
		print "Recording started "
		for i in range(0, 44100 / chunk * RECORD_SECONDS):
			data = stream.read(chunk)
			self.rec.append(data)
		recordOutput = wave.open("rec.wav", 'wb')
		recordOutput.setnchannels(CHANNELS)
		recordOutput.setsampwidth(sound.get_sample_size(FORMAT))
		recordOutput.setframerate(RATE)
		recordOutput.writeframes(b''.join(self.rec))
		recordOutput.close()
		print "Recording complete"
		stream.stop_stream()
		stream.close()
		sound.terminate()
		return

	def Mix(self,instance):
		ifile1=wave.open('output1.wav','r')
		num_channels1 = ifile1.getnchannels()
		sample_rate1 = ifile1.getframerate()
		sample_width1 = ifile1.getsampwidth()
		num_frames1 = ifile1.getnframes()
		raw_data1 = ifile1.readframes( num_frames1 )
		total_samples1 = num_frames1 * num_channels1

		if sample_width1 == 1: 
		   	fmt1 = "%iB" % total_samples1 # read unsigned chars
		elif sample_width1 == 2:
			fmt1 = "%ih" % total_samples1 # read signed 2 byte shorts
		else:
			raise ValueError("Only supports 8 and 16 bit audio formats.")

		sound1 = struct.unpack(fmt1, raw_data1)
	   	del raw_data1 
		sound1=list(sound1)

		ifile2=wave.open('output1.wav','r')
		num_channels2 = ifile2.getnchannels()
		sample_rate2 = ifile2.getframerate()
		sample_width2 = ifile2.getsampwidth()
		num_frames2 = ifile2.getnframes()
		raw_data2 = ifile2.readframes( num_frames2 )
		total_samples2 = num_frames2 * num_channels2

		if sample_width2 == 1: 
		   	fmt2 = "%iB" % total_samples2 # read unsigned chars
		elif sample_width2 == 2:
			fmt2 = "%ih" % total_samples2 # read signed 2 byte shorts
		else:
			raise ValueError("Only supports 8 and 16 bit audio formats.")

		sound2 = struct.unpack(fmt2, raw_data2)
	   	del raw_data2
		sound2=list(sound2)


		ifile3=wave.open('output3.wav','r')
		num_channels3 = ifile3.getnchannels()
		sample_rate3 = ifile3.getframerate()
		sample_width3 = ifile3.getsampwidth()
		num_frames3 = ifile3.getnframes()
		raw_data3 = ifile3.readframes( num_frames3 )
		total_samples3 = num_frames3 * num_channels3

		if sample_width3 == 1: 
			fmt3 = "%iB" % total_samples3 # read unsigned chars
		elif sample_width3 == 2:
			fmt3 = "%ih" % total_samples3 # read signed 2 byte shorts
		else:
			raise ValueError("Only supports 8 and 16 bit audio formats.")

		sound3 = struct.unpack(fmt3, raw_data3)
		del raw_data3 
		sound3=list(sound3)
	
		sum1=[]
		if len(sound1)<=len(sound2) and len(sound1)<=len(sound3):
			leng=len(sound1)
			flag=1
		elif len(sound2)<=len(sound3) and len(sound2)<=len(sound1):
			leng=len(sound2)
			flag=2
		elif len(sound3)<=len(sound2) and len(sound3)<=len(sound1):
			leng=len(sound3)
			flag=3

		for i in range(leng):
			sum1.append(sound1[i]+sound2[i]+sound3[i])
		k=i

		if flag==1:
			if len(sound2)<=len(sound3):
				leng=len(sound2)
				flag=2
			else:
			 	leng=len(sound3)
			 	flag=3
		
			for j in range(k,leng):
				sum1.append(sound2[j]+sound3[j])
			k=j
			if flag==2:
			  	for p in range(k,len(sound3)):
			 		sum1.append(sound3[p])
			else:
				for p in range(k,len(sound2)):
					sum1.append(sound2[p])
		elif flag==2:
			if len(sound1)<=len(sound3):
				leng=len(sound1)
				flag=1
			else:
			 	leng=len(sound3)
			 	flag=3
			for j in range(k,leng):
				sum1.append(sound1[j]+sound3[j])
			k=j
			if flag==1:
				for p in range(k,len(sound3)):
					sum1.append(sound3[p])
			else:
				for p in range(k,len(sound1)):
					sum1.append(sound1[p])

		elif flag==3:
			if len(sound2)<=len(sound1):
				leng=len(sound2)
				flag=2
			else:
			 	leng=len(sound1)
			 	flag=1
			for j in range(k,leng):
				sum1.append(sound2[j]+sound1[j])
			k=j
			if flag==2:
				for p in range(k,len(sound1)):
					sum1.append(sound1[p])
			else:
				for p in range(k,len(sound2)):
					sum1.append(sound2[p])

		if self.Mix1==1 and self.Mix2==1 and self.Mix3==0:
	       		for i in range(len(sound3)):
				sum1[i]-=sound3[i]

		elif self.Mix1==0 and self.Mix2==1 and self.Mix3==1:
			for i in range(len(sound1)):
				sum1[i]-=sound1[i]

		elif self.Mix1==1 and self.Mix2==0 and self.Mix3==0:
			for i in range(len(sound2)):
				sum1[i]-=sound2[i]

		elif self.Mix1==1 and self.Mix2==0 and self.Mix3==0:
			sum1=[]
			for i in range(len(sound1)):
				sum1.append(sound1[i])

		elif self.Mix1==0 and self.Mix2==1 and self.Mix3==0:
			sum1=[]
			for i in range(len(sound2)):
				sum1.append(sound2[i])

		elif self.Mix1==0 and self.Mix2==0 and self.Mix3==0:
			sum1=[]
			for i in range(len(sound3)):
				sum1.append(sound3[i])
		
		
		ofile = wave.open("outputmix.wav", "w")
		if self.Mix1==1:
			ofile.setparams(ifile1.getparams())
			if sample_width1==1:
				t=struct.pack('B'*len(sum1),*sum1)
			elif sample_width1==2:
				t=struct.pack('h'*len(sum1),*sum1)
		elif self.Mix2==1:
			ofile.setparams(ifile2.getparams())
			if sample_width2==1:
				t=struct.pack('B'*len(sum1),*sum1)
			elif sample_width2==2:
				t=struct.pack('h'*len(sum1),*sum1)
		elif self.Mix3==1:
			ofile.setparams(ifile3.getparams())
			if sample_width3==1:
				t=struct.pack('B'*len(sum1),*sum1)
			elif sample_width3==2:
				t=struct.pack('h'*len(sum1),*sum1)
			
		ofile.writeframes(t)
		ifile1.close()
		ifile2.close()
		ifile3.close()
		ofile.close()

		sound = SoundLoader.load('outputmix.wav')
		if sound:
			sound.play()

		return 
 
	def Modulate(self,instance):
		ifile1=wave.open('output1.wav','r')
		num_channels1 = ifile1.getnchannels()
	    	sample_rate1 = ifile1.getframerate()
	    	sample_width1 = ifile1.getsampwidth()
	    	num_frames1 = ifile1.getnframes()
		raw_data1 = ifile1.readframes( num_frames1 )
		total_samples1 = num_frames1 * num_channels1

	        if sample_width1 == 1: 
	        	fmt1 = "%iB" % total_samples1 # read unsigned chars
		elif sample_width1 == 2:
			fmt1 = "%ih" % total_samples1 # read signed 2 byte shorts
		else:
			raise ValueError("Only supports 8 and 16 bit audio formats.")

		sound1 = struct.unpack(fmt1, raw_data1)
    		del raw_data1 
		sound1=list(sound1)

		ifile2=wave.open('output2.wav','r')
		num_channels2 = ifile2.getnchannels()
	    	sample_rate2 = ifile2.getframerate()
	    	sample_width2 = ifile2.getsampwidth()
	    	num_frames2 = ifile2.getnframes()
		raw_data2 = ifile2.readframes( num_frames2 )
		total_samples2 = num_frames2 * num_channels2

	        if sample_width2 == 1: 
		        fmt2 = "%iB" % total_samples2 # read unsigned chars
		elif sample_width2 == 2:
			fmt2 = "%ih" % total_samples2 # read signed 2 byte shorts
		else:
			raise ValueError("Only supports 8 and 16 bit audio formats.")

		sound2 = struct.unpack(fmt2, raw_data2)
	    	del raw_data2 
		sound2=list(sound2)

		ifile3=wave.open('output3.wav','r')
		num_channels3 = ifile3.getnchannels()
	    	sample_rate3 = ifile3.getframerate()
	    	sample_width3 = ifile3.getsampwidth()
	    	num_frames3 = ifile3.getnframes()
		raw_data3 = ifile3.readframes( num_frames3 )
		total_samples3 = num_frames3 * num_channels3

	        if sample_width3 == 1: 
		        fmt3 = "%iB" % total_samples3 # read unsigned chars
		elif sample_width3 == 2:
			fmt3 = "%ih" % total_samples3 # read signed 2 byte shorts
		else:
			raise ValueError("Only supports 8 and 16 bit audio formats.")

		sound3 = struct.unpack(fmt3, raw_data3)
	    	del raw_data3 
		sound3=list(sound3)
		
		sum1=[]
		if len(sound1)<=len(sound2) and len(sound1)<len(sound3):
			leng=len(sound1)
			flag=1
		elif len(sound2)<=len(sound3) and len(sound2)<len(sound1):
			leng=len(sound2)
			flag=2
		elif len(sound3)<=len(sound2) and len(sound3)<len(sound1):
			leng=len(sound3)
			flag=3


		if self.Modulate1==1 and self.Modulate2==1 and self.Modulate3==1: 
			for i in range(leng):
				p=sound1[i]*sound2[i]*sound3[i]
				if p>32767:
					p=32767
				elif p<-32768:
					p=-32768
				sum1.append(p)
			k=i

			if flag==1:
				if len(sound2)<=len(sound3):
					leng=len(sound2)
					flag=2
				else:
			 		leng=len(sound3)
			 		flag=3
				for j in range(k,leng):
					p=sound2[i]*sound3[i]
					if p>32767:
						p=32767
					elif p<-32768:
						p=-32768
					sum1.append(p)
				k=j
				if flag==2:
					for p in range(k,len(sound3)):
						sum1.append(sound3[p])
				else:
					for p in range(k,len(sound2)):
						sum1.append(sound2[p])
			elif flag==2:
				if len(sound1)<=len(sound3):
					leng=len(sound1)
					flag=1
				else:
			 		leng=len(sound3)
			 		flag=3
				for j in range(k,leng):
					p=sound1[i]*sound3[i]
					if p>32767:
						p=32767
					elif p<-32768:
						p=-32768
					sum1.append(p)
				k=j
				if flag==1:
					for p in range(k,len(sound3)):
						sum1.append(sound3[p])
				else:
					for p in range(k,len(sound1)):
						sum1.append(sound1[p])

			elif flag==3:
				if len(sound2)<=len(sound1):
					leng=len(sound2)
					flag=2
				else:
			 		leng=len(sound1)
			 		flag=1
				for j in range(k,leng):
					p=sound1[i]*sound2[i]
					if p>32767:
						p=32767
					elif p<-32768:
						p=-32768
					sum1.append(p)
				k=j
				if flag==2:
					for p in range(k,len(sound1)):
						sum1.append(sound1[p])
				else:
					for p in range(k,len(sound2)):
						sum1.append(sound2[p])

		elif self.Modulate1==1 and self.Modulate2==1 and self.Modulate3==0:
	       			if len(sound1)<=len(sound2):
					leng=len(sound1)
					flag=1
				else: 
				 	leng=len(sound2)
				 	flag=2
				for i in range(leng):
					p=sound1[i]*sound2[i]
					if p>32767:
						p=32767
					elif p<-32768:
						p=-32768
					sum1.append(p)

				k=i;
				if flag==1:
					for i in range(k,len(sound2)):
						sum1.append(sound2[i])
				else:
					for i in range(k,len(sound1)):
						sum1.append(sound1[i])
				 
		elif self.Modulate1==0 and self.Modulate2==1 and self.Modulate3==1:
	       			if len(sound2)<=len(sound3):
					leng=len(sound2)
					flag=2
				else: 
				 	leng=len(sound3)
				 	flag=3
				for i in range(leng):
					p=sound3[i]*sound2[i]
					if p>32767:
						p=32767
					elif p<-32768:
						p=-32768
					sum1.append(p)
				k=i;
				if flag==2:
					for i in range(k,len(sound3)):
						sum1.append(sound3[i])
				else:
					for i in range(k,len(sound2)):
						sum1.append(sound2[i])

		elif self.Modulate1==1 and self.Modulate2==0 and self.Modulate3==1:
	       		if len(sound1)<=len(sound3):
				leng=len(sound1)
				flag=1
			else: 
			 	leng=len(sound3)
			 	flag=3
			for i in range(leng):
				p=sound1[i]*sound3[i]
				if p>32767:
					p=32767
				elif p<-32768:
					p=-32768
				sum1.append(p)
			k=i;
			if flag==1:
				for i in range(k,len(sound3)):
					sum1.append(sound3[i])
			else:
				for i in range(k,len(sound1)):
					sum1.append(sound1[i])

		elif self.Modulate1==1 and self.Modulate2==0 and self.Modulate3==0:
			for i in range(len(sound1)):
				sum1.append(sound1[i])

		elif self.Modulate1==0 and self.Modulate2==1 and self.Modulate3==0:
			for i in range(len(sound2)):
				sum1.append(sound2[i])

		elif self.Modulate1==0 and self.Modulate2==0 and self.Modulate3==0:
			for i in range(len(sound3)):
				sum1.append(sound3[i])
		
		
		ofile = wave.open("outputmod.wav", "w")
		if self.Modulate1==1:
			ofile.setparams(ifile1.getparams())
			if sample_width1==1:
				t=struct.pack('B'*len(sum1),*sum1)
			elif sample_width1==2:
				t=struct.pack('h'*len(sum1),*sum1)
		elif self.Modulate2==1:
			ofile.setparams(ifile2.getparams())
			if sample_width2==1:
				t=struct.pack('B'*len(sum1),*sum1)
			elif sample_width2==2:
				t=struct.pack('h'*len(sum1),*sum1)
		elif self.Modulate3==1:
			ofile.setparams(ifile3.getparams())
			if sample_width3==1:
				t=struct.pack('B'*len(sum1),*sum1)
			elif sample_width3==2:
				t=struct.pack('h'*len(sum1),*sum1)

			
		ofile.writeframes(t)
		ifile1.close()
		ifile2.close()
		ifile3.close()
		ofile.close()

		sound = SoundLoader.load('outputmod.wav')
		if sound:
			sound.play()

	def ampScale1(self,slider,value):
		self.slide1.value=value
	def tShift1(self,slider,value):
		self.slide2.value=value
	def tScale1(self,slider,value):
		self.slide3.value=value
	def ampScale2(self,slider,value):
		self.slide4.value=value
	def tShift2(self,slider,value):
		self.slide5.value=value
	def tScale2(self,slider,value):
		self.slide6.value=value
	def ampScale3(self,slider,value):
		self.slide7.value=value
	def tShift3(self,slider,value):
		self.slide8.value=value
	def tScale3(self,slider,value):
		self.slide9.value=value
	
	def on_checkbox_active1(self,checkbox,value):
		if value:
			self.tReverse1=1
		else :
			self.tReverse1 = 0
	def on_checkbox_active2(self,checkbox,value):
		if value:
			self.Modulate1=1
		else:
			self.Modulate1 = 0
	def on_checkbox_active3(self,checkbox,value):
		if value:
			self.Mix1=1
		else:
			self.Mix1 = 0
	def on_checkbox_active4(self,checkbox,value):
		if value:
			self.tReverse2=1
		else:
			self.tReverse2 = 0
	def on_checkbox_active5(self,checkbox,value):
		if value:
			self.Modulate2=1
		else:
			self.Modulate2 = 0
	def on_checkbox_active6(self,checkbox,value):
		if value:
			self.Mix2=1
		else:
			self.Mix2 = 0
	def on_checkbox_active7(self,checkbox,value):
		if value:
			self.tReverse3=1
		else:
			self.tReverse3 = 0
	def on_checkbox_active8(self,checkbox,value):
		if value:
			self.Modulate3=1
		else:
			self.Modulate3 = 0
	def on_checkbox_active9(self,checkbox,value):
		if value:
			self.Mix3=1
		else:
			self.Mix3 = 0


	def playSound1(self,instance):
		self.play1 = 1 - self.play1
		if self.play1 == 1:
			amplitude=self.slide1.value
			time_shift=self.slide2.value
			time_scale=self.slide3.value
			time_shift = int(time_shift)
			time_scale = int(time_scale)

			if(time_scale>=0 and time_scale<=10):
				time_scale=0.125
			if(time_scale>=10 and time_scale<=20):
				time_scale=0.250
			elif(time_scale>=20 and time_scale<=30):
				time_scale=0.50
			elif(time_scale>=30 and time_scale<=40):
				time_scale=0.00
			elif(time_scale>=40 and time_scale<=50):
				time_scale=2
			elif(time_scale>=50 and time_scale<=60):
				time_scale=4
			elif(time_scale>=60 and time_scale<=70):
				time_scale=8	
		
			ifile=wave.open(self.inputWaveFile1,'r')
			ofile = wave.open("output1.wav", "w")
			ofile.setparams(ifile.getparams())
			num_channels = ifile.getnchannels()
			sample_rate = ifile.getframerate()
			sample_width = ifile.getsampwidth()
			num_frames = ifile.getnframes()
		
			raw_data = ifile.readframes( num_frames )
			total_samples = num_frames * num_channels
			if sample_width == 1:
				fmt = "%iB" % total_samples # read unsigned chars
			elif sample_width == 2:
				fmt = "%ih" % total_samples # read signed 2 byte shorts
			else:
				raise ValueError("Only supports 8 and 16 bit audio formats.")
			l = struct.unpack(fmt, raw_data)
			del raw_data 
	
			l=list(l)
			for i in range(len(l)):
				if l[i]>=-32678 and l[i]<=32767:
					l[i]=l[i]*amplitude
				else:
					l[i]=32767

			d=[]
			if time_shift<0:
				time_shift*=-1
				for i in range(int(time_shift),len(l)):
					d.append(l[i])
				for i in range(0,int(time_shift)):
					d.append(0)
			elif(time_shift>=0):
				for i in range(0,int(time_shift)):
					d.append(0)
				for i in range(0,len(l)):
					d.append(l[i])
				
			l=[]
		
			if time_scale>1:
				for i in range(len(d)/time_scale):
					l.append(d[i*time_scale])

			elif time_scale<1 and time_scale!=0:
				time_scale=int(1/time_scale)
				for i in range(len(d)):
					for j in range(time_scale):
						l.append(d[i])

			elif time_scale==0:
				for i in range(len(d)):
					l.append(d[i])
		
			if(self.tReverse1==1):
				l.reverse()
		
			if sample_width==1:
				t=struct.pack('B'*len(l),*l)
			elif sample_width==2:
				t=struct.pack('h'*len(l),*l)
			
			ofile.writeframes(t)
			ifile.close()
			ofile.close()
			self.sound1 = SoundLoader.load('output1.wav')
			if self.sound1:
				self.sound1.play()
		elif self.play1 == 0:
			self.sound1.stop()		
	

	def playSound2(self,instance):
		self.play2 = 1 - self.play2
		if self.play2 == 1:
			amplitude=self.slide4.value
			time_shift=self.slide5.value
			time_scale=self.slide6.value
			time_shift=int(time_shift)
			time_scale=int(time_scale)

			if(time_scale>=0 and time_scale<=10):
				time_scale=0.125
			if(time_scale>=10 and time_scale<=20):
				time_scale=0.250
			elif(time_scale>=20 and time_scale<=30):
				time_scale=0.50
			elif(time_scale>=30 and time_scale<=40):
				time_scale=0.00
			elif(time_scale>=40 and time_scale<=50):
				time_scale=2
			elif(time_scale>=50 and time_scale<=60):
				time_scale=4
			elif(time_scale>=60 and time_scale<=70):
				time_scale=8	
		
			ifile=wave.open(self.inputWaveFile2,'r')
			ofile = wave.open("output2.wav", "w")
			ofile.setparams(ifile.getparams())
			num_channels = ifile.getnchannels()
			sample_rate = ifile.getframerate()
			sample_width = ifile.getsampwidth()
			num_frames = ifile.getnframes()
		
			raw_data = ifile.readframes( num_frames )
			total_samples = num_frames * num_channels

			if sample_width == 1: 
				fmt = "%iB" % total_samples # read unsigned chars
			elif sample_width == 2:
				fmt = "%ih" % total_samples # read signed 2 byte shorts
			else:
				raise ValueError("Only supports 8 and 16 bit audio formats.")

			l = struct.unpack(fmt, raw_data)	
			del raw_data 
				
			l=list(l)
			for i in range(len(l)):
				if l[i]>=-32678 and l[i]<=32767:
					l[i]=l[i]*amplitude
				else:
					l[i]=32767
			d=[]
			if time_shift<0:
				time_shift*=-1
				for i in range(int(time_shift),len(l)):
					d.append(l[i])
				for i in range(0,int(time_shift)):
					d.append(0)
			elif(time_shift>=0):
				for i in range(0,int(time_shift)):
					d.append(0)
				for i in range(0,len(l)):
					d.append(l[i])
		
			l=[]

			if time_scale>1:
				for i in range(len(d)/time_scale):
					l.append(d[i*time_scale])

			elif time_scale<1 and time_scale!=0:
				time_scale=int(1/time_scale)
				for i in range(len(d)):
					for j in range(time_scale):
						l.append(d[i])

			elif time_scale==0:
				for i in range(len(d)):
					l.append(d[i])
		
			if(self.tReverse2==1):
				l.reverse()
	        
			if sample_width==1:
				t=struct.pack('B'*len(l),*l)
			elif sample_width==2:
				t=struct.pack('h'*len(l),*l)
			
			ofile.writeframes(t)
			ifile.close()
			ofile.close()

			self.sound2 = SoundLoader.load('output2.wav')
			if self.sound2:
				self.sound2.play()

		if self.play2 == 0:
			self.sound2.stop()

	def playSound3(self,instance):
		self.play3 = 1 - self.play3
		if self.play3 == 1:
			amplitude=self.slide7.value
			time_shift=self.slide8.value
			time_scale=self.slide9.value
			time_shift=int(time_shift)
			time_scale=int(time_scale)

			if(time_scale>=0 and time_scale<=10):
				time_scale=0.125
			if(time_scale>=10 and time_scale<=20):
				time_scale=0.250
			elif(time_scale>=20 and time_scale<=30):
				time_scale=0.50
			elif(time_scale>=30 and time_scale<=40):
				time_scale=0.00
			elif(time_scale>=40 and time_scale<=50):
				time_scale=2
			elif(time_scale>=50 and time_scale<=60):
				time_scale=4
			elif(time_scale>=60 and time_scale<=70):
				time_scale=8	
		
			ifile=wave.open(self.inputWaveFile3,'r')
			ofile = wave.open("output3.wav", 'w')
			ofile.setparams(ifile.getparams())
			num_channels = ifile.getnchannels()
			sample_rate = ifile.getframerate()
			sample_width = ifile.getsampwidth()
			num_frames = ifile.getnframes()
			raw_data = ifile.readframes( num_frames )
			total_samples = num_frames * num_channels

			if sample_width == 1: 
			    fmt = "%iB" % total_samples # read unsigned chars
			elif sample_width == 2:
				fmt = "%ih" % total_samples # read signed 2 byte shorts
			else:
				raise ValueError("Only supports 8 and 16 bit audio formats.")

			l = struct.unpack(fmt, raw_data)
	    		del raw_data 

		
			l=list(l)
			for i in range(len(l)):
				if l[i]>=-32678 and l[i]<=32767:
					l[i]=l[i]*amplitude
				else:
					l[i]=32767

			d=[]
			if time_shift<0:
				time_shift*=-1
				for i in range(int(time_shift),len(l)):
					d.append(l[i])
				for i in range(0,int(time_shift)):
					d.append(0)
			elif(time_shift>=0):
				for i in range(0,int(time_shift)):
					d.append(0)
				for i in range(0,len(l)):
					d.append(l[i])
	
			l=[]
			if time_scale>1:
				for i in range(len(d)/time_scale):
					l.append(d[i*time_scale])

			elif time_scale<1 and time_scale!=0:
				time_scale=int(1/time_scale)
				for i in range(len(d)):
					for j in range(time_scale):
						l.append(d[i])

			elif time_scale==0:
				for i in range(len(d)):
					l.append(d[i])

			if(self.tReverse3==1):
				l.reverse()
	    
			if sample_width==1:
				t=struct.pack('B'*len(l),*l)
			elif sample_width==2:
				t=struct.pack('h'*len(l),*l)
			
			ofile.writeframes(t)
			ifile.close()
			ofile.close()
			self.sound3 = SoundLoader.load('output3.wav')
			if self.sound3:
				self.sound3.play()
		if self.play3 == 0:
			self.sound3.stop()	 

	def selectSound3(self, instance):
		content = BoxLayout(orientation='vertical', spacing=5)
		self.popup = popup = Popup(title='Wave Mixer', content=content, size_hint=(None, None), size=(600, 400))
		self.scrollView = scrollView = ScrollView()
		self.fileChooser = fileChooser = FileChooserListView(size_hint_y=None, path = '/home/')
		fileChooser.bind(on_submit=self._validate3)
		fileChooser.height = 1500 
		scrollView.add_widget(fileChooser)
		content.add_widget(Widget(size_hint_y=None, height=5))
		content.add_widget(scrollView)
		content.add_widget(Widget(size_hint_y=None, height=5))
		btnlayout = BoxLayout(size_hint_y=None, height=50, spacing=5)
		btn = Button(text='Ok')
		btn.bind(on_press=partial(self._validate3, fileChooser))
		btnlayout.add_widget(btn)
		btn = Button(text='Cancel')
		btn.bind(on_release=popup.dismiss)
		btnlayout.add_widget(btn)
		content.add_widget(btnlayout)
		popup.open()

	def selectSound1(self, instance):
		content = BoxLayout(orientation='vertical', spacing=5)
		self.popup = popup = Popup(title='Wave Mixer', content=content, size_hint=(None, None), size=(600, 400))
		self.scrollView = scrollView = ScrollView()
		self.fileChooser = fileChooser = FileChooserListView(size_hint_y=None, path = '/home/')
		fileChooser.bind(on_submit=self._validate1)
		fileChooser.height = 1500 
		scrollView.add_widget(fileChooser)
		content.add_widget(Widget(size_hint_y=None, height=5))
		content.add_widget(scrollView)
		content.add_widget(Widget(size_hint_y=None, height=5))
		btnlayout = BoxLayout(size_hint_y=None, height=50, spacing=5)
		btn = Button(text='Ok')
		btn.bind(on_press=partial(self._validate1, fileChooser))
		btnlayout.add_widget(btn)
		btn = Button(text='Cancel')
		btn.bind(on_release=popup.dismiss)
		btnlayout.add_widget(btn)
		content.add_widget(btnlayout)
		popup.open()

	def selectSound2(self, instance):
		content = BoxLayout(orientation='vertical', spacing=5)
		self.popup = popup = Popup(title='Wave Mixer', content=content, size_hint=(None, None), size=(600, 400))
		self.scrollView = scrollView = ScrollView()
		self.fileChooser = fileChooser = FileChooserListView(size_hint_y=None, path = '/home/')
		fileChooser.bind(on_submit=self._validate2)
		fileChooser.height = 1500 
		scrollView.add_widget(fileChooser)
		content.add_widget(Widget(size_hint_y=None, height=5))
		content.add_widget(scrollView)
		content.add_widget(Widget(size_hint_y=None, height=5))
		btnlayout = BoxLayout(size_hint_y=None, height=50, spacing=5)
		btn = Button(text='Ok')
		btn.bind(on_press=partial(self._validate2, fileChooser))
		btnlayout.add_widget(btn)
		btn = Button(text='Cancel')
		btn.bind(on_release=popup.dismiss)
		btnlayout.add_widget(btn)
		content.add_widget(btnlayout)
		popup.open()

	def _validate1(self, fileChooser, selected):		
		value = fileChooser.selection
		self.popup.dismiss()
		self.popup = None
		if value == '':
			return
		else:
			value = str(value)
			x = value.split('/')
			x = x[len(x) - 1]
			inputFile = x.split('\'')[0]
			y = inputFile.split('.')
			if(y[1] != 'wav'):
				exit(0)
			else:
				self.inputWaveFile1 = inputFile

	def _validate2(self, fileChooser, selected):	
		value = fileChooser.selection
		self.popup.dismiss()
		self.popup = None
		if value == '':
			return
		else:
			value = str(value)
			x = value.split('/')
			x = x[len(x) - 1]
			inputFile = x.split('\'')[0]
			y = inputFile.split('.')
			if(y[1] != 'wav'):
				exit(0)
			else:
				self.inputWaveFile2 = inputFile

	def _validate3(self, fileChooser, selected):
		value = fileChooser.selection
		self.popup.dismiss()
		self.popup = None
		if value == '':
			return
		else:
			value = str(value)
			x = value.split('/')
			x = x[len(x) - 1]
			inputFile = x.split('\'')[0]
			y = inputFile.split('.')
			if(y[1] != 'wav'):
				exit(0)
			else:
				self.inputWaveFile3 = inputFile
	
class MyApp(App):
	title = 'Wave Mixer'
	def build(self):
		return WaveApp()

if __name__ == '__main__':
	    MyApp().run()
		

