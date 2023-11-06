SLOW_START = "slow start"
CONGESTION_AVOIDANCE = "congestion avoidance"

class CongestionControl:
    def __init__(self, MSS : int) -> None:
        self.current_state = SLOW_START
        self.MSS = MSS
        self.cwnd = MSS
        self.ssthresh = None

    def get_cwnd(self) -> int:
        """Retorna la cantidad de bytes que caben en la ventana"""
        return self.cwnd
    
    def get_MSS_in_cwnd(self) -> int:
        """Retorna la cantidad de segmentos de tamaño máximo caben en la ventana"""
        return self.cwnd // self.MSS
    
    def event_ack_received(self) -> None:
        """Maneja el recibimiento de un ACK"""
        # El estado es slow start
        if self.current_state == SLOW_START:
            # cwnd aumenta un MSS cada vez que llega un ACK
            self.cwnd += self.MSS
            # Si ya ha ocurrido un timeout y cwnd es sobrepasa a ssthresh, se pasa a congestion avoidance
            if not self.ssthresh is None and self.cwnd >= self.ssthresh:
                self.current_state = CONGESTION_AVOIDANCE

        # El estado es congestion avoidance
        else:
            self.cwnd += self.MSS / self.get_MSS_in_cwnd()


    def event_timeout(self) -> None:
        if self.current_state == SLOW_START and self.ssthresh is None:
            # Se utiliza la función techo de la divición por dos para la asignación de ssthresh
            self.ssthresh = self.cwnd // 2
            self.cwnd = self.MSS

        elif self.current_state == CONGESTION_AVOIDANCE:
            self.current_state = SLOW_START

            # Se utiliza la función techo de la divición por dos para la asignación de ssthresh
            self.ssthresh = self.cwnd // 2
            self.cwnd = self.MSS

    def is_state_slow_start(self):
        return self.current_state == SLOW_START
    
    def is_state_congestion_avoidance(self):
        return self.current_state == CONGESTION_AVOIDANCE
    
    def get_ssthresh(self):
        return self.ssthresh