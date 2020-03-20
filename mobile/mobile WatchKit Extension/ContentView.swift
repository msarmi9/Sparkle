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

    var body: some View {
        VStack {
            HStack {
                Image(systemName: "star.fill")

                Text("Sparkle")
                    .font(.system(size: 32)).italic()

                Image(systemName: "star.fill")
            }

            Spacer()
                .frame(height: 25)
            
            Button(action: {
                self.isRecording.toggle()
            }) {
                isRecording ? Text("Stop Recording"): Text("Start Recording")
                
            }
            
            if isRecording {
                HStack {
                    Image(systemName: "play.fill")
                        .font(.headline).foregroundColor(.green)
                        Text("Recording Data")
                    }
                }
            
            else {
                HStack {
                Image(systemName: "stop.fill")
                    .font(.headline).foregroundColor(.red)
                    Text("Recording Data")
                }

            }

            HStack {
                Image(systemName: "antenna.radiowaves.left.and.right")
                    .font(.headline)
                // maybe want to use a button here..
                NavigationLink(destination: SensorView()){
                    Text("See sensors")
                }
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
