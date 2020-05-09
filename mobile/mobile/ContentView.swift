//
//  SensorView.swift
//  mobile WatchKit Extension
//
//  Created by Collin Prather on 3/20/20.
//  Copyright © 2020 Collin Prather. All rights reserved.
//

import SwiftUI
import Alamofire

let loginParameters: [String: String] = [
"patient_id": "2"
]

struct rxMetadata: Decodable {
    let firstname: String
    let timestamp: String
    let drug: String
    let desc: String
    let amount: Int
}

//func sendLoginPost(patient_id: String, _ completion: @escaping (String?, String?, String?, String?, Int?) -> Void){
//    let parameters = ["patient_id": patient_id]
//    AF.request("http://http://sparkle-env-1.eba-b8vqgrb3.us-west-2.elasticbeanstalk.com/mobile-login",
//               method: .post,
//               parameters: parameters,
//               encoder: JSONParameterEncoder.default).responseDecodable(of: [rxMetadata].self) { response in
////                    debugPrint(response)
//                guard let schedule = response.value else { return }
//                let firstname = schedule[0].firstname
//                let timestamp = schedule[0].timestamp
//                let drug = schedule[0].drug
//                let desc = schedule[0].desc
//                let amount = schedule[0].amount
//                completion(firstname, timestamp, drug, desc, amount)
//    }
//}

// to catch the index out of range error
extension Collection {
    subscript(safe index: Index) -> Element? {
        return indices.contains(index) ? self[index] : nil
    }
}


class ContentViewModel: ObservableObject {
    // https://www.calincrist.com/blog/2020-04-12-how-to-get-notified-for-changes-in-swiftui/
    var patient_id: String = "" {
        willSet { // only updates view if patient_id > 1
            if patient_id.count > 1  {
                self.sendLoginPost()
                objectWillChange.send()
            }
        }
    }
    @Published var firstname: String = "" {
        didSet {
            loggedIn = (firstname.count > 1)
        }
    }
    @Published var nextTime: String = ""
    @Published var nextDrug: String = ""
    @Published var nextDesc: String = ""
    @Published var nextAmount: Int = 0
    @Published var attemptedLogIn: Bool = false
    @Published var loggedIn: Bool = false
    
    func sendLoginPost(){
        let parameters = ["patient_id": self.patient_id]
        AF.request("http://sparkle-env-1.eba-b8vqgrb3.us-west-2.elasticbeanstalk.com/mobile-login",
                   method: .post,
                   parameters: parameters,
                   encoder: JSONParameterEncoder.default).responseDecodable(of: [rxMetadata].self) { response in
                        debugPrint(response)
                    guard let schedule = response.value else { return }
                    self.attemptedLogIn = true
                    if schedule.count > 0 {
                        self.firstname = schedule[0].firstname
                        self.nextTime = schedule[0].timestamp
                        self.nextDrug = schedule[0].drug
                        self.nextDesc = schedule[0].desc
                        self.nextAmount = schedule[0].amount
                    }
                    
//                    completion(self.firstname, self.nextTime, self.nextDrug, self.nextDesc, self.nextAmount)
        }
    }
}

func parseTime(ts: String) -> String {
    let hour = ts[String.Index(utf16Offset: 11, in:ts)...String.Index(utf16Offset: 13, in: ts)]
    if hour == "20" {
        return "8 pm"
    } else {
        return "8 am"
    }
}


extension Text {
    func customTitleText() -> some View {
        self
            .fontWeight(.bold)
            .font(.title)
            .padding()
            .cornerRadius(40)
            .foregroundColor(.white)
            .padding(10)
    }
}


// View
struct ContentView: View {
    @ObservedObject var viewModel = ContentViewModel()
    @State private var showNext: Bool = false
    @ObservedObject var watchSession: WatchSessionManager
    @State private var showingWelcome = false
    
    var body: some View {
        VStack {
            Image("logo_new")
                .resizable()
                .scaledToFit()
                .padding(25)
            if self.viewModel.loggedIn == false {  // logged out
                TextField("Enter patient id here",
                          text: $viewModel.patient_id,
                          onCommit: { self.viewModel.sendLoginPost()
                })
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding(25)
                
                if self.viewModel.attemptedLogIn == true {
                    Text("It doesn't look like you're registered yet!")
                }
                
                ZStack {
                    RoundedRectangle(cornerRadius: 25)
                    .fill(Color.black)
                    .frame(width: 325, height: 100)
                    .shadow(color: Color("sparkleColor").opacity(0.2), radius: 10, x: 10, y: 10)
                    .shadow(color: Color("sparkleColor").opacity(0.7), radius: 10, x: -5, y: -5)
                    
                    Text("Welcome!")
                            .font(.title)
                            .foregroundColor(.white)
                }
                 .padding(50)
                
                ////////////////////////////////////////////////////////
                VStack {
                    Toggle(isOn: $showingWelcome.animation(.easeInOut(duration: 3))) {
                        Text("Toggle label")
                    }.padding(EdgeInsets(top: 10, leading: 50, bottom: 10, trailing: 50))

                    if showingWelcome {
                        Text("Hello World")
                    }
                }
                ////////////////////////////////////////////////////////
                
            } else {                               // logged in
                Toggle(isOn: $viewModel.loggedIn) {
                    Text("You're logged in")
                }.padding(EdgeInsets(top: 10, leading: 50, bottom: 10, trailing: 50))
                
                Text("Welcome, \(viewModel.firstname)!")
                    .font(.headline)
                    .italic()
                    .padding(EdgeInsets(top: 10, leading: 50, bottom: 10, trailing: 50))
                
                ZStack {
                    RoundedRectangle(cornerRadius: 25)
                    .fill(Color.black)
                    .frame(width: 325, height: 100)
                    .shadow(color: Color("sparkleColor").opacity(0.2), radius: 10, x: 10, y: 10)
                    .shadow(color: Color("sparkleColor").opacity(0.7), radius: 10, x: -5, y: -5)
                    
                    Button(action: {
                        self.showNext = true
                    }) {
                        Text("Get today's schedule")
                            .customTitleText()
                    }
                    .alert(isPresented: $showNext) {
                        Alert(title: Text("Next medication:"), message: Text("Don't forget to take \(viewModel.nextAmount) \(viewModel.nextDrug)'s at \(parseTime(ts: viewModel.nextTime)) today!"), dismissButton: .default(Text("Got it!")))
                    }
                }.padding(.bottom, 35)
                
                
                ZStack {
                    RoundedRectangle(cornerRadius: 25)
                    .fill(Color.black)
                    .frame(width: 325, height: 275)
                    .shadow(color: Color("sparkleColor").opacity(0.2), radius: 10, x: 10, y: 10)
                    .shadow(color: Color("sparkleColor").opacity(0.7), radius: 10, x: -5, y: -5)
                    
                    VStack {
                        Text("Record an intake")
                            .customTitleText()
                        
                        TextField("Prescription id",
                        text: $watchSession.prescription_id).padding(EdgeInsets(top: 0, leading: 50, bottom: 0, trailing: 50))
                        
                        Toggle("Intake on time", isOn: $watchSession.onTime).padding(EdgeInsets(top: 0, leading: 50, bottom: 20, trailing: 50))
                        
                        Text("Status:")
                            .font(.title)
                            .foregroundColor(.white)
                        
                        if self.watchSession.pred_string == "You haven't taken medication recently." {
                            Text(watchSession.pred_string)
                                .italic()
                                .foregroundColor(.white)
                                .padding(.bottom, 35)
                        } else {
                            Text(watchSession.pred_string)
                                .italic()
                                .foregroundColor(Color("sparkleColorAccent"))
                                .padding(.bottom, 35)

                        }
                        
                            
                    }
                    
                }
                
                
            }
            
            
            Spacer()
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
    @ObservedObject var viewModel: ContentViewModel
    var body: some View {
        NavigationView {
            HStack {
                    Image(systemName: "antenna.radiowaves.left.and.right")
                        .font(.headline)
                    // maybe want to use a button here..
                    NavigationLink(destination: SensorLogView(watchSession: WatchSessionManager())){
                        Text("See recent intakes")
                    }
            }
        }
    }
}

struct SensorView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView(watchSession: WatchSessionManager()).background(Color(UIColor.systemBackground))
        .environment(\.colorScheme, .dark)
    }
}
