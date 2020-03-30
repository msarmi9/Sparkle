//
//  SensorView.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 3/20/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI


// View
struct ContentView: View {
    

    var body: some View {
        VStack {
            Title()
            Spacer().frame(height: 25)
            SeeSensors()
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

struct SeeSensors: View {
    var body: some View {
        NavigationView {
            HStack {
                Image(systemName: "antenna.radiowaves.left.and.right")
                    .font(.headline)
                // maybe want to use a button here..
                NavigationLink(destination: SensorLogView(watchSession: WatchSessionManager())){
                    Text("See sensors")
                }
            }
        }
    }
}

struct SensorView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
