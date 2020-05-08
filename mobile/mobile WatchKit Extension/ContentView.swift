//
//  ContentView.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 3/20/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI

struct ContentView: View {
    @State private var isRecording: Bool = false // UI changes when this variable changes
    @ObservedObject var motion: MotionManager
    @State private var duration: Float = 0.0
    @State var Hz: Int =  30
    @State var pillCount: String = "1"
    

    var body: some View {
        ScrollView {
            VStack {
                Title()
                Spacer().frame(height: 23)
                if isRecording {
                    // When isRecording = True
                    VStack {
                        isRecordingTrue(isRecording: $isRecording,
                                        motion: motion,
                                        duration: $duration,
                                        pillCount: $pillCount)
                        DurationView(duration: $duration)
                        }
                } else {
                    isRecordingFalse(isRecording: $isRecording,
                                     motion: motion,
                                     duration: $duration,
                                     Hz: $Hz,
                                     pillCount: $pillCount)
                }
//                MetaDataView(motion: motion,
//                             Hz: $Hz,
//                             pillCount: $pillCount)
            }
        }
    }
}

struct Title: View {
    var body: some View {
        Image("logo")
        .resizable()
        .scaledToFit()
    }
}


struct isRecordingFalse: View {
    @Binding var isRecording: Bool
    @ObservedObject var motion: MotionManager
    @Binding var duration: Float
    @Binding var Hz: Int
    @Binding var pillCount: String

    var body: some View {
        HStack {
            Image(systemName: "calendar")
            
            Button(action: {
                self.isRecording.toggle()
                self.motion.reset()
                self.motion.startUpdates(Hz: 1.0/Double(self.Hz), pillCount: self.pillCount)
                self.duration = 0.0
            }) {
                Text("Take a pill")
            }
        }
    }
}


struct isRecordingTrue: View {
    @Binding var isRecording: Bool
    @ObservedObject var motion: MotionManager
    @Binding var duration: Float
    @Binding var pillCount: String
    var body: some View {
        HStack {
            Image(systemName: "calendar")
                .foregroundColor(Color.green)
            
            Button(action: {
                // Not sure what the order of these lines of code should be
                self.isRecording.toggle()
                self.motion.stopUpdates()
                self.motion.sendMessage(sensorData: ["sensorString": self.motion.sensorString, "pillCount": String(self.pillCount)])
            }) {
                Text("Stop recording")
            }
        }
    }
}


struct DurationView: View {
    @Binding var duration: Float
    let timer = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()

    var body: some View {
        Text("\(String(format: "Duration: %.1f", duration))")
            .onReceive(timer) { input in
                self.duration = self.duration + 0.1
            }
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView(motion: MotionManager())
    }
}
