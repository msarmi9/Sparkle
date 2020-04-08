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
    @State private var currentTime: TimeInterval = 0.0

    var body: some View {
        VStack {
            Title()
            Spacer().frame(height: 25)
            RecordingButton(isRecording: $isRecording)
            if isRecording {
                RecordingStatus(isRecording: $isRecording)
                Text("\(currentTime)")
                // resume @ 21 mins in WWDC19 Data Flow video
                // for now, viewing WWDC19 Combine in practice
            }
            SeeSensors()
        }
    }
}

struct Title: View {
    var body: some View {
        HStack {
            Image(systemName: "star.fill")

            Text("0.0.4")
                .font(.system(size: 32)).italic()

            Image(systemName: "star.fill")
        }
    }
}

struct RecordingButton: View {
    @Binding var isRecording: Bool
    var body: some View {
        Button(action: {
            withAnimation{ self.isRecording.toggle() }
        }) {
            isRecording ? Text("Stop Recording"): Text("Start Recording")
            
        }
    }
}

struct RecordingStatus: View {
    @Binding var isRecording: Bool
    var body: some View {
        VStack {
            if isRecording {
                RecordingYes(isRecording: $isRecording)
                }
            
            else {
                RecordingNo(isRecording: $isRecording)

            }
        }
    }
}

struct RecordingYes: View {
    @Binding var isRecording: Bool
    var body: some View {
        HStack {
        Image(systemName: "play.fill")
            .font(.headline).foregroundColor(.green)
            Text("Recording Data")
        }
    }
}

struct RecordingNo: View {
    @Binding var isRecording: Bool
    var body: some View {
        HStack {
        Image(systemName: "stop.fill")
            .font(.headline).foregroundColor(.red)
            Text("Recording Data")
        }
    }
}

struct SeeSensors: View {
    var body: some View {
        HStack {
            Image(systemName: "antenna.radiowaves.left.and.right")
                .font(.headline)
            // maybe want to use a button here..
            NavigationLink(destination: SensorView(motion: MotionManager())){
                Text("See sensors")
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
