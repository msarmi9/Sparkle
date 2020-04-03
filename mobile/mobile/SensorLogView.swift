//
//  SensorLogView.swift
//  mobile
//
//  Created by Collin Prather on 3/30/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI
import Combine
import WatchConnectivity


// struct to display list of messages sent to s3
struct Message: Identifiable {
    var id = UUID()
    var dateString: String
}

class WatchMessages: ObservableObject {
    @Published
    var messagesReceived: [Any] = []
    
    
}




struct SensorLogView: View {
//    @ObservedObject
//    var watchSession: WatchSessionManager
    
    var body: some View {
        Text("Lots to add")
//        List(watchSession.messagesReceived) { message in
//            Text(message.dateString)
        }
    }

struct SensorLogView_Previews: PreviewProvider {
    static var previews: some View {
        SensorLogView()
    }
}
