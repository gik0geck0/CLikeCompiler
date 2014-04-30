module CLikeTypes where

-- data Program
newtype Type = Type [String]
    deriving Show

modifyType :: String -> Type -> Type
modifyType s (Type v) = Type (s:v)

data Term =
      TermValue Part
    | TermMult Part Part
    | TermDiv  Part Part
    | TermLSh  Part Part
    | TermRSh  Part Part
    deriving Show

data Part =
      PartID String
    | PartNum Int
    deriving Show
