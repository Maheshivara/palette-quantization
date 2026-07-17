from enum import Enum, auto

from core.domain.distance import DistanceCalculator
from core.distance.cielab import CIELABDistanceCalculator
from core.distance.delta_e2000 import DeltaE2000DistanceCalculator
from core.distance.delta_e94 import DeltaE94DistanceCalculator
from core.distance.hsv import HSVDistanceCalculator
from core.distance.manhattan import ManhattanDistanceCalculator
from core.distance.red_mean import RedMeanDistanceCalculator
from core.distance.sqr_euclidean import SQREuclideanDistanceCalculator
from core.distance.wgt_euclidean import WGTEuclideanDistanceCalculator


class DistanceType(Enum):
    SQR_EUCLIDEAN = auto()
    WGT_EUCLIDEAN = auto()
    MANHATTAN = auto()
    RED_MEAN = auto()
    HSV_DISTANCE = auto()
    CIELAB = auto()
    DELTA_E94 = auto()
    DELTA_E2000 = auto()


class DistanceCalculatorFactory:
    @staticmethod
    def create(type: DistanceType) -> DistanceCalculator:
        match type:
            case DistanceType.CIELAB:
                return CIELABDistanceCalculator()

            case DistanceType.DELTA_E2000:
                return DeltaE2000DistanceCalculator()

            case DistanceType.DELTA_E94:
                return DeltaE94DistanceCalculator()

            case DistanceType.HSV_DISTANCE:
                return HSVDistanceCalculator()

            case DistanceType.MANHATTAN:
                return ManhattanDistanceCalculator()

            case DistanceType.RED_MEAN:
                return RedMeanDistanceCalculator()

            case DistanceType.SQR_EUCLIDEAN:
                return SQREuclideanDistanceCalculator()

            case DistanceType.WGT_EUCLIDEAN:
                return WGTEuclideanDistanceCalculator()
