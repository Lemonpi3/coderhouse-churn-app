import pandas as pd

#Este archivo contiene las clases de los modelos para evitar errores de importacion

class Model_1:
    '''Clase del modelo de clasificacción multiple'''
    import pandas as pd

    def __init__(self, pipeline, model):
        self.pipeline = pipeline
        self.model = model
    
    def clean_nulls_dataset(self, df:pd.DataFrame, cols_to_drop:list)->tuple:
        '''Reemplaza Nulos numericos con 0 y Categoricos con No
        Retorna copia del imputado df limpio y lista de indices de las variables categoricas'''
        import pandas as pd

        df = df[df.columns.difference(cols_to_drop)].copy()
        categorical_cols = []
        categorical_idx = []
        num_cols = []

        #como se q no va haber nulos en la demo de la app comento todo esto pq me estaba dando errores
        # for i,col in enumerate(df.columns):
        #     if df[col].dtypes.str=='|O':
        #         categorical_idx.append(i)
        #         categorical_cols.append(col)
        #     else:
        #         num_cols.append(i)

        # null_status = df.isna().sum()

        # for col in categorical_cols:
        #     df[col].fillna('No',inplace=True)
        # for col in num_cols:
        #     df[col].fillna(0,inplace=True)

        # null_status = df.isna().sum()

        return df , categorical_idx

    def predict(self, df:pd.DataFrame)->pd.DataFrame:
        '''Retorna las predict proba de cada categoria'''
        data, _ = self.clean_nulls_dataset(df,['customer_id','city','zip_code','churn_category','churn_reason', 'customer_status'])
        data = self.pipeline.transform(data)

        out_dict = {
            'churn_chance': []
        }

        preds = self.model.predict_proba(data)
        preds = preds.round(2) * 100
        out_dict['churn_chance'] = [ pred[0] for pred in preds ] #Getting churn chance for the predictions
        
        return pd.DataFrame(out_dict)

class Model_2:
    '''Clase del modelo de clasificacción multiple'''
    import pandas as pd

    def __init__(self, pipeline, model):
        self.pipeline = pipeline
        self.model = model
    
    def clean_nulls_dataset(self, df:pd.DataFrame, cols_to_drop:list)->tuple:
        '''Reemplaza Nulos numericos con 0 y Categoricos con No
        Retorna copia del imputado df limpio y lista de indices de las variables categoricas'''
        import pandas as pd

        
        df = df[df.columns.difference(cols_to_drop)].copy()
        categorical_cols = []
        categorical_idx = []
        num_cols = []
        #como se q no va haber nulos en la demo de la app comento todo esto pq me estaba dando errores

        # for i,col in enumerate(df.columns):
        #     if df[col].dtypes.str=='|O':
        #         categorical_idx.append(i)
        #         categorical_cols.append(col)
        #     else:
        #         num_cols.append(i)

        # null_status = df.isna().sum()

        # for col in categorical_cols:
        #     df[col].fillna('No',inplace=True)
        # for col in num_cols:
        #     df[col].fillna(0,inplace=True)

        # null_status = df.isna().sum()

        return df , categorical_idx

    def predict(self, df:pd.DataFrame)->pd.DataFrame:
        '''Retorna las predict proba de cada categoria'''
        data, _ = self.clean_nulls_dataset(df,['customer_id'])
        data = self.pipeline.transform(data)

        preds = self.model.predict_proba(data)[:len(data)]

        out_dict = {
            'attitude_reason_chance':[],
            'competitor_reason_chance':[],
            'dissatisfaction_reason_chance':[],
            'other_reason_chance':[],
            'price_reason_chance':[],
        }

        for pred in preds:
            out_dict['attitude_reason_chance'].append(round(pred[0]*100,2))
            out_dict['competitor_reason_chance'].append(round(pred[1]*100,2))
            out_dict['dissatisfaction_reason_chance'].append(round(pred[2]*100,2))
            out_dict['other_reason_chance'].append(round(pred[3]*100,2))
            out_dict['price_reason_chance'].append(round(pred[4]*100,2))

        return pd.DataFrame(out_dict)

class Total_Revenue_Regressor:
    def __init__(self, pipe, model):
        self.pipe = pipe
        self.model = model

    def clean_nulls_dataset(self,df:pd.DataFrame,cols_to_drop:list)->tuple:
        '''Reemplaza Nulos numericos con 0 y Categoricos con No
        
        Retorna copia del imputado df limpio y lista de indices de las variables categoricas'''

        df = df[df.columns.difference(cols_to_drop)].copy()
        categorical_cols = []
        categorical_idx = []
        num_cols = []

        for i,col in enumerate(df.columns):
            if df[col].dtypes.str=='|O':
                categorical_cols.append(col)
                categorical_idx.append(list(df.columns).index(col))
            else:
                num_cols.append(col)

        null_status = df.isna().sum()

        for col in categorical_cols:
            df[col].fillna('No',inplace=True)
        for col in num_cols:
            df[col].fillna(0,inplace=True)

        null_status = df.isna().sum()

        return df , categorical_idx

    def predict(self,df):
        df, cat_idx = self.clean_nulls_dataset(df,['customer_id','city','zip_code',
                                    'total_charges', 'total_refunds', 'total_extra_data_charges',	
                                    'total_long_distance_charges','total_revenue']) #saco total revenue por si las dudas
        
        X = self.pipe.transform(df)
        return self.model.predict(X)

class Client_Clusterer:

    def __init__(self, pipe, model):
        self.pipe = pipe
        self.model = model

    def clean_nulls_dataset(self,df:pd.DataFrame,cols_to_drop:list)->tuple:
        '''Reemplaza Nulos numericos con 0 y Categoricos con No
        
        Retorna copia del imputado df limpio y lista de indices de las variables categoricas'''

        df = df[df.columns.difference(cols_to_drop)].copy()
        categorical_cols = []
        categorical_idx = []
        num_cols = []

        for i,col in enumerate(df.columns):
            if df[col].dtypes.str=='|O':
                categorical_cols.append(col)
                categorical_idx.append(list(df.columns).index(col))
            else:
                num_cols.append(col)

        null_status = df.isna().sum()

        for col in categorical_cols:
            df[col].fillna('No',inplace=True)
        for col in num_cols:
            df[col].fillna(0,inplace=True)

        null_status = df.isna().sum()

        return df , categorical_idx

    def predict(self,df):
        df, cat_idx = self.clean_nulls_dataset(df,['customer_id','city','zip_code','churn_category','churn_reason', 'customer_status'])
        
        scaler_cols = ['age', 'number_of_dependents','avg_monthly_long_distance_charges',
               'avg_monthly_gb_download', 'monthly_charge', 'total_charges',
               'total_extra_data_charges', 'total_long_distance_charges', 'total_revenue',
               'number_of_referrals', 'tenure_in_months', 'total_refunds','latitude', 'longitude']

        df[scaler_cols] = self.pipe.transform(df[scaler_cols])
        clusters = self.model.predict(df, categorical=cat_idx)
        return clusters