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
    

    var body: some View {
        VStack {
            Title()
            Spacer().frame(height: 25)
            if isRecording {
                // When isRecording = True
                VStack {
                    isRecordingTrue(isRecording: $isRecording,
                                    motion: motion,
                                    duration: $duration)
                    DurationView(duration: $duration)
                    }
            } else {
                isRecordingFalse(isRecording: $isRecording,
                                 motion: motion,
                                 duration: $duration)
            }
        }
    }
}

struct Title: View {
    var body: some View {
        HStack {
            Image(systemName: "star.fill")

            Text("Sparkle")
                .font(.system(size: 32)).italic()

            Image(systemName: "star.fill")
        }
    }
}


struct isRecordingFalse: View {
    @Binding var isRecording: Bool
    @ObservedObject var motion: MotionManager
    @Binding var duration: Float
    var body: some View {
        HStack {
            Image(systemName: "calendar")
            
            Button(action: {
                self.isRecording.toggle()
                self.motion.reset()
                self.motion.startUpdates(Hz: 1.0/5)
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
    var body: some View {
        HStack {
            Image(systemName: "calendar")
                .foregroundColor(Color.green)
            
            Button(action: {
                // Not sure what the order of these lines of code should be
                self.isRecording.toggle()
                self.motion.stopUpdates()
                self.motion.sendMessage(sensorData: ["sensorString": self.motion.sensorString])
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
