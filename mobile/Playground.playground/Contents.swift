import SwiftUI
import PlaygroundSupport

struct DurationView: View {
    @State var duration = 0.0
    let timer = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()

    var body: some View {
        Text("\(String(format: "Duration: %.1f", duration))")
            .onReceive(timer) { input in
                self.duration = self.duration + 0.1
            }
    }
}


//struct ContentView: View {
//    @State var timeRemaining = 10
//    let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()
//
//    var body: some View {
//        Text("\(timeRemaining)")
//            .onReceive(timer) { _ in
//                if self.timeRemaining > 0 {
//                    self.timeRemaining -= 1
//                }
//            }
//    }
//}

PlaygroundPage.current.setLiveView(DurationView())
